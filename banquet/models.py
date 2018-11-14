import uuid
from django.db import models
from django.contrib.auth.models import User

from companies.models import Company
from people.models import DietaryRestriction
from accounting.models import Product
from fair.models import Fair


class Banquet(models.Model):
	fair = models.ForeignKey(Fair, on_delete = models.CASCADE)
	name = models.CharField(max_length = 75, blank = False, null = False)
	date = models.DateTimeField()
	location = models.CharField(max_length = 75, blank = True, null = True)
	dress_code = models.CharField(max_length = 255, blank = True, null = True)
	caption_phone_number = models.CharField(max_length = 255, blank = True, null = True, verbose_name = 'Caption for the phone number field')
	caption_dietary_restrictions = models.CharField(max_length = 255, blank = True, null = True, verbose_name = 'Caption for dietary restrictions')
	product = models.ForeignKey(Product, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Product to link the banquet with')
	
	def __str__(self): return self.name


class Table(models.Model):
	banquet = models.ForeignKey(Banquet, on_delete = models.CASCADE)
	name = models.CharField(max_length = 75, blank = False, null = False)
	
	class Meta:
		unique_together = [['banquet', 'name']]
	
	def __str__(self): return self.name


class Seat(models.Model):
	table = models.ForeignKey(Table, on_delete = models.CASCADE)
	name = models.CharField(max_length = 75, blank = False, null = False)
	
	class Meta:
		unique_together = [['table', 'name']]
	
	def __str__(self): return self.table.name + ' ' + self.name


class Participant(models.Model):
	banquet = models.ForeignKey(Banquet, on_delete = models.CASCADE)
	company = models.ForeignKey(Company, blank = True, null = True, on_delete = models.CASCADE)
	user = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE)
	name = models.CharField(max_length = 75, blank = True, null = True)	     # None if a user is provided, required for others
	email_address = models.EmailField(max_length = 75, blank = True, null = True, verbose_name = 'E-mail address') # None if a user is provided, required for others
	phone_number = models.CharField(max_length = 75, blank = True, null = True)  # None if a user is provided, required for others
	dietary_restrictions = models.ManyToManyField(DietaryRestriction, blank = True)
	alcohol = models.BooleanField(choices = [(True, 'Yes'), (False, 'No')], default = True)
	seat = models.OneToOneField(Seat, blank = True, null = True, on_delete = models.CASCADE)
	charge_stripe = models.CharField(max_length = 255, blank = True, null = True) # set if the participant has paid for their participation
	
	def __str__(self): return (self.name + ' (' + self.company.name + ')') if self.company else (self.name if self.name else str(self.user))


class InvitationGroup(models.Model):
	banquet = models.ForeignKey(Banquet, on_delete = models.CASCADE)
	name = models.CharField(max_length = 255, null = False, blank = False, unique = True)
	deadline = models.DateField(null = True, blank = True)
	
	def __str__(self): return self.name


class Invitation(models.Model):
	banquet = models.ForeignKey(Banquet, on_delete = models.CASCADE)
	group = models.ForeignKey(InvitationGroup, on_delete = models.CASCADE)
	token = models.CharField(max_length = 255, null = False, blank = False, default = uuid.uuid4, unique = True)
	user = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE, related_name = 'banquet_invitation_user')
	participant = models.ForeignKey(Participant, blank = True, null = True, on_delete = models.CASCADE) # filled in when the participant has been created from this invitation
	name = models.CharField(max_length = 75, blank = True, null = True)
	email_address = models.CharField(max_length = 75, blank = True, null = True)
	reason = models.CharField(max_length = 75, blank = True, null = True)
	price = models.PositiveIntegerField(verbose_name = 'Price (SEK)') # can be zero
	denied = models.BooleanField(default = False)
	deadline = models.DateField(null = True, blank = True)
	
	@property
	def deadline_smart(self):
		return self.deadline if self.deadline is not None else self.group.deadline
	
	@property
	def status(self):
		if self.participant is not None: return 'GOING'
		elif self.denied: return 'NOT_GOING'
		else: return 'PENDING'

	@classmethod
	def create(cls, banquet, participant, name, email_address, reason, price, user):
		return cls(
			banquet=banquet,
			participant=participant,
			name=name,
			email_address=email_address,
			reason=reason,
			price=price,
			user=user,
		)

	def __str__(self): return (self.name if self.name is not None else str(self.user))


class AfterPartyTicket(models.Model):
	token = models.CharField(max_length = 255, null = False, blank = False, default = uuid.uuid4, unique = True)
	name = models.CharField(max_length = 75, blank = True, null = True)
	email_address = models.EmailField(max_length = 75, blank = True, null = True, verbose_name = 'E-mail address')
	charge_stripe = models.CharField(max_length = 255, blank = True, null = True)
	paid_timestamp = models.DateTimeField(null = True, blank = True)
	paid_price = models.PositiveIntegerField(null = True, blank = True)
	
	def __str__(self): return self.name + ' <' + self.email_address + '> -- ' + str(self.token)
