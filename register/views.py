import requests as r
import json

from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.forms.models import inlineformset_factory, HiddenInput

from companies.models import Company, CompanyContact, Group, CompanyCustomerComment
from exhibitors.models import Exhibitor
from fair.models import Fair, FairDay, LunchTicket
from companies.forms import CompanyForm, InitialCompanyContactForm, CreateCompanyContactForm, CreateCompanyContactNoCompanyForm, UserForm
from accounting.models import Product, Order, RegistrationSection
from banquet.models import Participant as BanquetParticipant
from banquet.models import Banquet
from django.contrib.auth.models import User

from .models import SignupContract, SignupLog
from .forms import InitialInterestsRegistrationForm, InitialCommentForm, InitialRegistrationForm, CompleteCompanyDetailsForm, CompleteLogisticsDetailsForm, CompleteCatalogueDetailsForm, NewCompanyForm, CompleteProductQuantityForm, CompleteProductBooleanForm, CompleteFinalSubmissionForm, RegistrationForm, ChangePasswordForm, TransportForm, LunchTicketForm, BanquetParticipantForm

from .help.methods import get_time_flag


def choose_company(request):
	if not request.user.is_authenticated():
		fair = Fair.objects.filter(current = True).first()
		initial_not_open = timezone.now() < fair.registration_start_date

		return render(request, 'register/outside/login_or_register.html',
		{
			'fair': fair,
			'initial_not_open': initial_not_open,
		})

	# find all connections between this user and companies
	company_contacts = CompanyContact.objects.filter(user = request.user).exclude(company = None)

	if len(company_contacts) == 1: return redirect('anmalan:registration', company_contacts.first().company.pk)

	# if zero or several company_contacts connections
	return render(request, 'register/choose_company.html', {'company_contacts': company_contacts})


def form(request, company_pk):
	if not request.user.is_authenticated(): return redirect('anmalan:logout')

	company = get_object_or_404(Company, pk = company_pk)
	fair = Fair.objects.filter(current = True).first()
	exhibitor = Exhibitor.objects.filter(fair = fair, company = company).first()

	if request.user.has_perm('companies.base') or (exhibitor is not None and (request.user.has_perm('exhibitors.view_all') or request.user in exhibitor.contact_persons.all())):
		company_contact = None

	else:
		company_contact = CompanyContact.objects.filter(user = request.user, company = company).first()

		if not company_contact: return redirect('anmalan:choose_company')

	if timezone.now() < fair.registration_start_date: return render(request, 'register/inside/error_before_initial.html',
	{
		'fair': fair,
		'company': company,
		'company_contact': company_contact,
	})

	# show IR template if IR has opened and CR has not opened (=> we could be between IR and CR)
	if timezone.now() >= fair.registration_start_date and timezone.now() < fair.complete_registration_start_date: return form_initial(request, company, company_contact, fair)

	# we're in or after CR! perhaps the company did not complete their IR?
	signature = SignupLog.objects.filter(company = company, contract__fair = fair, contract__type = 'INITIAL')
	if len(signature) == 0: return render(request, 'register/inside/error_after_initial_no_signature.html',
	{
		'fair': fair,
		'company': company,
		'company_contact': company_contact,
	})

	# ...or perhaps they weren't selected to participate in this year's fair?
	if exhibitor is None: return render(request, 'register/inside/error_after_initial_no_exhibitor.html',
	{
		'fair': fair,
		'company': company,
		'company_contact': company_contact,
	})

	return form_complete(request, company, company_contact, fair, exhibitor)


def form_initial(request, company, company_contact, fair):
	contract = SignupContract.objects.filter(fair = fair, type = 'INITIAL').first()
	signature = SignupLog.objects.filter(company = company, contract__fair = fair, contract__type = 'INITIAL').first()
	deadline = fair.registration_end_date
	# admin_user used as author of comment on company which will be imported in CRM system
	admin_user = User.objects.filter(first_name = "admin", last_name = "admin", email = "support@armada.nu").first()

	# form is bounded (request.POST) if the post has to do with the form in question
	# form_initial_registration is unbound (no parameter) since no existing data can be connected to the form
	form_initial_interests = InitialInterestsRegistrationForm(request.POST if request.POST and request.POST.get('save_initial_registration') else None)
	form_initial_comment = InitialCommentForm(request.POST if request.POST and request.POST.get('save_initial_registration') else None)
	form_initial_registration = InitialRegistrationForm()

	form_company_details = NewCompanyForm(request.POST if request.POST and request.POST.get('save_company_details') else None, instance = company)
	form_company_contact = InitialCompanyContactForm(request.POST if request.POST and request.POST.get('save_contact_details') else None, instance = company_contact)

	is_editable = timezone.now() >= fair.registration_start_date and timezone.now() <= fair.registration_end_date
	# only company contacts can edit the form - maybe add extra security feature that the company_contact should be active (or confirmed for complete registration?)
	is_authorized = company_contact != None

	if request.POST:
		if request.POST.get('save_company_details') and form_company_details.is_valid() and is_authorized:
			form_company_details.save()
			form_company_details = NewCompanyForm(instance = company)

		elif request.POST.get('save_contact_details') and form_company_contact.is_valid() and is_authorized:
			form_company_contact.save()
			form_company_contact = InitialCompanyContactForm(instance = company_contact)

		elif request.POST.get('save_initial_registration') and is_editable and is_authorized and signature is None:
			if form_initial_interests.is_valid():
				added_groups = form_initial_interests.cleaned_data['groups']
				for group in added_groups:
					company.groups.add(group)

			if form_initial_comment.is_valid():
				input_comment = form_initial_comment.cleaned_data['text_input']
			if input_comment:
				comment = CompanyCustomerComment.objects.create(
					company = company,
					user = admin_user,
					comment = 'INITIAL REGISTRATION: '+input_comment,
					show_in_exhibitors = False
				)

			signature = SignupLog.objects.create(company_contact = company_contact, contract = contract, company = company)


	if not is_authorized or not is_editable:
		for field in form_initial_registration.fields: form_initial_registration.fields[field].disabled = True

	if not is_authorized:
		for field in form_company_details.fields: form_company_details.fields[field].disabled = True
		for field in form_company_contact.fields: form_company_contact.fields[field].disabled = True

	return render(request, 'register/inside/registration_initial.html',
	{
		'fair': fair,
		'company': company,
		'company_contact': company_contact,
		'contract': contract,
		'signature': signature,
		'deadline': deadline,
		'form_company_details': form_company_details,
		'form_initial_registration': form_initial_registration,
		'form_company_contact': form_company_contact,
		'form_initial_interests': form_initial_interests,
		'form_initial_comment': form_initial_comment,
		'is_editable': is_editable,
		'is_authorized': is_authorized,
	})


def form_complete(request, company, company_contact, fair, exhibitor):
	contract = SignupContract.objects.filter(fair = fair, type = 'COMPLETE').first()
	signature = SignupLog.objects.filter(company = company, contract__fair = fair, contract__type = 'COMPLETE').first()

	form_company_details = CompleteCompanyDetailsForm(request.POST if request.POST and request.POST.get('save_company_details') else None, instance = company)
	form_logistics_details = CompleteLogisticsDetailsForm(request.POST if request.POST and request.POST.get('save_logistics_details') else None, instance = exhibitor)
	form_catalogue_details = CompleteCatalogueDetailsForm(request.POST if request.POST.get('save_catalogue_details') else None, request.FILES if request.POST.get('save_catalogue_details') else None, instance = exhibitor)
	form_final_submission = CompleteFinalSubmissionForm(request.POST if request.POST and request.POST.get('save_final_submission') else None)

	orders = Order.objects.filter(purchasing_company = company, unit_price = None, name = None)

	deadline = exhibitor.deadline_complete_registration or fair.complete_registration_close_date

	is_editable = timezone.now() >= fair.complete_registration_start_date and timezone.now() <= deadline

	# hosts can never edit the form
	if company_contact is None and not request.user.has_perm('companies.base'): is_editable = False

	# exhibitor representatives cannot edit orders if they have received at least one invoice
	can_edit_orders = Order.objects.filter(purchasing_company = company, product__revenue__fair = fair).exclude(export_batch = None).count() == 0

	registration_sections = []

	for registration_section_raw in RegistrationSection.objects.all():
		registration_section = {
			'name': registration_section_raw.name,
			'description': registration_section_raw.description,
			'products': []
		}

		for product_raw in Product.objects.select_related('category').filter(revenue__fair = fair, registration_section = registration_section_raw):
			quantity_initial = 0

			for order in orders:
				if order.product == product_raw:
					quantity_initial += order.quantity

			if product_raw.max_quantity == 1:
				form_product = CompleteProductBooleanForm(request.POST if request.POST and request.POST.get('save_product_' + str(product_raw.id)) else None, prefix = 'product_' + str(product_raw.id), initial = {'checkbox': True if quantity_initial == 1 else False})
				if not is_editable or not can_edit_orders: form_product.fields['checkbox'].disabled = True

			else:
				form_product = CompleteProductQuantityForm(request.POST if request.POST and request.POST.get('save_product_' + str(product_raw.id)) else None, prefix = 'product_' + str(product_raw.id))
				form_product.fields['quantity'].choices = [(i, i) for i in range(0, (product_raw.max_quantity + 1) if product_raw.max_quantity is not None else 21)]
				form_product.fields['quantity'].initial = quantity_initial

				if not is_editable or not can_edit_orders: form_product.fields['quantity'].disabled = True

			if request.POST and request.POST.get('save_product_' + str(product_raw.id)) and form_product.is_valid() and is_editable and can_edit_orders:
				quantity = (1 if form_product.cleaned_data['checkbox'] else 0) if product_raw.max_quantity == 1 else int(form_product.cleaned_data['quantity'])

				if quantity == 0:
					for order in Order.objects.filter(purchasing_company = company, product = product_raw, unit_price = None, name = None):
						order.delete()

				else:
					order_all = Order.objects.filter(purchasing_company = company, product = product_raw, unit_price = None, name = None)

					if len(order_all) == 1:
						order = order_all.first()
						order.quantity = quantity

					elif len(order_all) > 1:
						for o in order:
							o.delete()

					if len(order_all) != 1: order = Order(purchasing_company = company, product = product_raw, quantity = quantity)

					order.save()

			product = {
				'id': product_raw.id,
				'name': product_raw.name,
				'description': product_raw.description,
				'category': product_raw.category.name if product_raw.category else None,
				'unit_price': product_raw.unit_price,
				'max_quantity': product_raw.max_quantity,
				'form': form_product
			}

			registration_section['products'].append(product)

		registration_sections.append(registration_section)

	if signature:
		form_logistics_details.fields['booth_height'].required = True
		form_logistics_details.fields['electricity_total_power'].required = True
		form_logistics_details.fields['electricity_socket_count'].required = True
		form_catalogue_details.fields['catalogue_about'].required = True
		form_catalogue_details.fields['catalogue_purpose'].required = True
		form_catalogue_details.fields['catalogue_logo_squared'].required = True

	if request.POST:
		if request.POST.get('save_company_details') and form_company_details.is_valid() and is_editable:
			form_company_details.save()
			form_company_details = CompleteCompanyDetailsForm(instance = company)

		elif request.POST.get('save_logistics_details') and form_logistics_details.is_valid() and is_editable:
			form_logistics_details.save()
			form_logistics_details = CompleteLogisticsDetailsForm(instance = exhibitor)

		elif request.POST.get('save_catalogue_details') and form_catalogue_details.is_valid() and is_editable:
			form_catalogue_details.save()
			form_catalogue_details = CompleteCatalogueDetailsForm(instance = exhibitor)

		elif request.POST.get('save_final_submission') and form_final_submission.is_valid() and signature is None:
			signature = SignupLog.objects.create(company_contact = company_contact, contract = contract, company = company)

	form_company_details.fields['invoice_name'].widget.attrs['placeholder'] = company.name

	orders = []
	orders_total = 0

	for order in Order.objects.filter(product__revenue__fair = fair, purchasing_company = company):
		unit_price = order.product.unit_price if order.unit_price is None else order.unit_price

		orders_total += order.quantity * unit_price

		orders.append(
		{
			'category': order.product.category.name if order.product.category else None,
			'name': order.product.name if order.name is None else order.name,
			'description': order.product.description if order.product.registration_section is None else None,
			'quantity': order.quantity,
			'unit_price': unit_price
		})

	errors = []

	if not company.has_invoice_address(): errors.append('Invoice address')
	if not exhibitor.booth_height: errors.append('Height of booth (cm)')
	if exhibitor.electricity_total_power is None: errors.append('Total power needed (W)')
	if exhibitor.electricity_socket_count is None: errors.append('Number of power sockets required')
	if not exhibitor.catalogue_about: errors.append('Short text about the company')
	if not exhibitor.catalogue_purpose: errors.append('Text about the purpose of the company')
	if not exhibitor.catalogue_logo_squared: errors.append('Squared logotype')

	if signature:
		for field in form_company_details.fields: form_company_details.fields[field].disabled = True

	if not is_editable:
		for field in form_company_details.fields: form_company_details.fields[field].disabled = True
		for field in form_logistics_details.fields: form_logistics_details.fields[field].disabled = True
		for field in form_catalogue_details.fields: form_catalogue_details.fields[field].disabled = True

	return render(request, 'register/inside/registration_complete.html',
	{
		'fair': fair,
		'contract': contract,
		'company': company,
		'company_contact': company_contact,
		'exhibitor': exhibitor,
		'form_company_details': form_company_details,
		'form_logistics_details': form_logistics_details,
		'form_catalogue_details': form_catalogue_details,
		'registration_sections': registration_sections,
		'orders': orders,
		'orders_total': orders_total,
		'errors': errors,
		'form_final_submission': form_final_submission,
		'signature': signature,
		'deadline': deadline,
		'is_editable': is_editable
	})


def create_user(request, template_name='register/outside/create_user.html'):
	contact_form = CreateCompanyContactForm(request.POST or None, prefix='contact')
	user_form = UserForm(request.POST or None, prefix='user')

	if request.POST and contact_form.is_valid() and user_form.is_valid():
		user = user_form.save(commit=False)
		contact = contact_form.save(commit=False)
		user.username = contact.email_address
		user.email = contact.email_address
		user.save()
		contact.user = user
		contact.save()
		user = authenticate(username=contact_form.cleaned_data['email_address'], password=user_form.cleaned_data['password1'],)
		login(request, user)
		return redirect('anmalan:choose_company')

	return render(request, template_name, dict(contact_form=contact_form, user_form=user_form))


def create_company(request, template_name='register/outside/create_company.html'):
	form = NewCompanyForm(request.POST or None)
	contact_form = CreateCompanyContactNoCompanyForm(request.POST or None, prefix='contact')
	user_form = UserForm(request.POST or None, prefix='user')

	if contact_form.is_valid() and user_form.is_valid() and form.is_valid():
		company = form.save()
		user = user_form.save(commit=False)
		contact = contact_form.save(commit=False)
		user.username = contact.email_address
		user.email = contact.email_address
		user.save()
		contact.user = user
		contact.confirmed = True #Auto confirm contacts who register a new company
		contact.company = company
		contact.save()
		user = authenticate(username=contact_form.cleaned_data['email_address'], password=user_form.cleaned_data['password1'],)
		login(request, user)
		return redirect('anmalan:choose_company')
	return render(request, template_name, dict(form=form, contact_form=contact_form, user_form=user_form))


def change_password(request, template_name='register/change_password.html'):
	if request.method == 'POST':
		form = ChangePasswordForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect('anmalan:choose_company')
		else:
			return redirect('anmalan:change_password')
	else:
		form = ChangePasswordForm(user=request.user)

	return render(request, template_name, {'registration': form})


def preliminary_registration(request, fair, company, contact, contract, exhibitor, signed_up, allow_saving):
	form = RegistrationForm((request.POST or None) if allow_saving else None, prefix = 'registration', instance = company)

	if not signed_up and form.is_valid():
		form.cleaned_data["groups"] = company.groups.filter(fair = fair).union(form.cleaned_data["groups"])
		form.save()
		SignupLog.objects.create(company_contact = contact, contract = contract, company = contact.company)

		return redirect('anmalan:choose_company')

	return ('register/registration.html', dict(registration_open = True, signed_up = signed_up, contact = contact, company=company, exhibitor = exhibitor, fair=fair, form = form, contract_url = contract.contract.url if contract else None ))


def transport(request, company_pk):
	if not request.user.is_authenticated(): return redirect('anmalan:logout')

	company = get_object_or_404(Company, pk = company_pk)
	fair = Fair.objects.filter(current = True).first()
	exhibitor = get_object_or_404(Exhibitor, fair = fair, company = company)

	if request.user.has_perm('companies.base') or (exhibitor is not None and (request.user.has_perm('exhibitors.view_all') or request.user in exhibitor.contact_persons.all())):
		company_contact = None
		initial = {}

	else:
		company_contact = CompanyContact.objects.filter(user = request.user, company = company).first()

		if not company_contact: return redirect('anmalan:choose_company')

		initial = {
			'contact_name': (company_contact.first_name + ' ' + company_contact.last_name) if (company_contact.first_name and company_contact.last_name) else None,
			'contact_email_address': company_contact.user.email,
			'contact_phone_number': company_contact.mobile_phone_number if company_contact.mobile_phone_number is not None else company_contact.work_phone_number
		}

	form = TransportForm(request.POST or None, initial = initial)

	if request.POST and form.is_valid() and True == False: # TODO: not used in 2018, but perhaps in 2019?
		body = [
			'Company name: ' + company.name + ' (' + str(company.pk) + ')',
			'Contact person: ' + form.cleaned_data['contact_name'],
			'Phone number: ' + form.cleaned_data['contact_phone_number'],
			'',
			'Description of parcels:',
			form.cleaned_data['description_of_parcels'],
			'',
			'Address details:',
			form.cleaned_data['address_details']
		]

		email = EmailMessage(
			'Transport request from ' + company.name,
			'\n'.join(body),
			'info@armada.nu',
			['armada@ryskaposten.se'],
			['support@armada.nu'],
			cc = [form.cleaned_data['contact_email_address']],
			reply_to = [form.cleaned_data['contact_email_address']]
		)

		email.send()

		form = None

	return render(request, 'register/inside/transport.html',
	{
		'fair': fair,
		'company': company,
		'company_contact': company_contact,
		'exhibitor': exhibitor,
		'form': form
	})


def lunchtickets(request, company_pk):
	if not request.user.is_authenticated(): return redirect('anmalan:logout')

	company = get_object_or_404(Company, pk = company_pk)
	fair = Fair.objects.filter(current = True).first()
	exhibitor = get_object_or_404(Exhibitor, fair = fair, company = company)

	if request.user.has_perm('companies.base') or (exhibitor is not None and (request.user.has_perm('exhibitors.view_all') or request.user in exhibitor.contact_persons.all())):
		company_contact = None

	else:
		company_contact = CompanyContact.objects.filter(user = request.user, company = company).first()

		if not company_contact: return redirect('anmalan:choose_company')

	count_ordered = 0

	for order in Order.objects.filter(purchasing_company = exhibitor.company, product = exhibitor.fair.product_lunch_ticket):
		count_ordered += order.quantity

	days = []
	count_created = 0

	for day in FairDay.objects.filter(fair = fair):
		lunch_tickets = LunchTicket.objects.filter(company = exhibitor.company, day = day)
		count_created += len(lunch_tickets)

		days.append({
			'date': day.date,
			'lunch_tickets': lunch_tickets
		})

	return render(request, 'register/inside/lunchtickets.html',
	{
		'fair': fair,
		'company': company,
		'company_contact': company_contact,
		'exhibitor': exhibitor,
		'days': days,
		'can_create': count_ordered > count_created,
		'count_ordered': count_ordered,
		'count_created': count_created
	})


def lunchtickets_form(request, company_pk, lunch_ticket_pk = None):
	if not request.user.is_authenticated(): return redirect('anmalan:logout')

	company = get_object_or_404(Company, pk = company_pk)
	fair = Fair.objects.filter(current = True).first()
	exhibitor = get_object_or_404(Exhibitor, fair = fair, company = company)

	if request.user.has_perm('companies.base') or (exhibitor is not None and (request.user.has_perm('exhibitors.view_all') or request.user in exhibitor.contact_persons.all())):
		company_contact = None

	else:
		company_contact = CompanyContact.objects.filter(user = request.user, company = company).first()

		if not company_contact: return redirect('anmalan:choose_company')

	is_editable = company_contact is not None or request.user.has_perm('companies.base')

	lunch_ticket = get_object_or_404(LunchTicket, pk = lunch_ticket_pk, company = company) if lunch_ticket_pk is not None else None

	count_ordered = 0

	for order in Order.objects.filter(purchasing_company = exhibitor.company, product = exhibitor.fair.product_lunch_ticket):
		count_ordered += order.quantity

	count_created = LunchTicket.objects.filter(company = company).count()

	if lunch_ticket is not None or count_ordered > count_created:
		form = LunchTicketForm(request.POST or None, instance = lunch_ticket, initial = {
			'company': company,
			'fair': exhibitor.fair
		})

		form.fields['email_address'].required = True

		if not is_editable:
			for field in form.fields: form.fields[field].disabled = True

		if request.POST and form.is_valid() and is_editable:
			form.instance.fair = exhibitor.fair
			form.instance.company = company
			form.save()

			return redirect('anmalan:lunchtickets', company.pk)

	else:
		form = None

	return render(request, 'register/inside/lunchtickets_form.html',
	{
		'fair': fair,
		'company': company,
		'company_contact': company_contact,
		'exhibitor': exhibitor,
		'form': form,
		'is_editable': is_editable
	})


def banquet(request, company_pk):
	if not request.user.is_authenticated(): return redirect('anmalan:logout')

	company = get_object_or_404(Company, pk = company_pk)
	fair = Fair.objects.filter(current = True).first()
	exhibitor = Exhibitor.objects.filter(fair = fair, company = company).first()

	if request.user.has_perm('companies.base') or (exhibitor is not None and (request.user.has_perm('exhibitors.view_all') or request.user in exhibitor.contact_persons.all())):
		company_contact = None

	else:
		company_contact = CompanyContact.objects.filter(user = request.user, company = company).first()

		if not company_contact: return redirect('anmalan:choose_company')

	count_ordered = 0

	for banquet in Banquet.objects.filter(fair = fair).exclude(product = None):
		for order in Order.objects.filter(purchasing_company = company, product = banquet.product):
			count_ordered += order.quantity

	banquets = []
	count_created = 0

	for banquet in Banquet.objects.filter(fair = fair):
		banquet_tickets = BanquetParticipant.objects.filter(company = company, banquet = banquet)
		count_created += len(banquet_tickets)

		banquets.append({
			'name': banquet.name,
			'banquet_tickets': banquet_tickets
		})

	return render(request, 'register/inside/banquet.html',
	{
		'fair': fair,
		'company': company,
		'company_contact': company_contact,
		'exhibitor': exhibitor,
		'banquets': banquets,
		'can_create': count_ordered > count_created,
		'count_ordered': count_ordered,
		'count_created': count_created
	})


def banquet_form(request, company_pk, banquet_participant_pk = None):
	if not request.user.is_authenticated(): return redirect('anmalan:logout')

	company = get_object_or_404(Company, pk = company_pk)
	fair = Fair.objects.filter(current = True).first()
	exhibitor = get_object_or_404(Exhibitor, fair = fair, company = company)

	if request.user.has_perm('companies.base') or (exhibitor is not None and (request.user.has_perm('exhibitors.view_all') or request.user in exhibitor.contact_persons.all())):
		company_contact = None

	else:
		company_contact = CompanyContact.objects.filter(user = request.user, company = company).first()

		if not company_contact: return redirect('anmalan:choose_company')

	is_editable = company_contact is not None or request.user.has_perm('companies.base')

	banquet_participant = get_object_or_404(BanquetParticipant, pk = banquet_participant_pk, company = company) if banquet_participant_pk is not None else None

	banquets = []

	for banquet in Banquet.objects.filter(fair = fair).exclude(product = None):
		count_ordered = 0
		count_created = BanquetParticipant.objects.filter(company = company, banquet = banquet).count()

		for order in Order.objects.filter(purchasing_company = company, product = banquet.product):
			count_ordered += order.quantity

		if count_ordered > count_created: banquets.append(banquet)

	if banquet_participant is not None or len(banquets) > 0:
		if banquet_participant is not None and banquet_participant.banquet not in banquets: banquets.append(banquet_participant.banquet)

		form = BanquetParticipantForm(request.POST or None, instance = banquet_participant, initial = {'company': company, 'banquet': banquets[0]})

		form.fields['banquet'].choices = [(banquet.pk, banquet.name) for banquet in banquets]

		# not required by the model since student participants shouldn't have them, but company representatives always need to
		form.fields['name'].required = True
		form.fields['email_address'].required = True
		form.fields['phone_number'].required = True

		if len(banquets) == 1:
			form.fields['banquet'].widget = HiddenInput()

		if not is_editable:
			for field in form.fields: form.fields[field].disabled = True

		if request.POST and form.is_valid() and is_editable:
			form.instance.company = company
			form.save()

			return redirect('anmalan:banquet', company.pk)

	else:
		form = None

	return render(request, 'register/inside/banquet_form.html',
	{
		'fair': fair,
		'company': company,
		'company_contact': company_contact,
		'exhibitor': exhibitor,
		'form': form,
		'is_editable': is_editable
	})


def events(request, company_pk):
	if not request.user.is_authenticated(): return redirect('anmalan:logout')

	company = get_object_or_404(Company, pk = company_pk)
	fair = Fair.objects.filter(current = True).first()

	if request.user.has_perm('companies.base'):
		company_contact = None

	else:
		company_contact = CompanyContact.objects.filter(user = request.user, company = company).first()

		if not company_contact: return redirect('anmalan:choose_company')

	exhibitor = Exhibitor.objects.filter(fair = fair, company = company).first()

	return render(request, 'register/inside/events.html',
	{
		'fair': fair,
		'company': company,
		'company_contact': company_contact,
		'exhibitor': exhibitor
	})
