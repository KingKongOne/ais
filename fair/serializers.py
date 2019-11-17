def lunch_ticket(lunch_ticket):
    data = {
        'id': lunch_ticket.pk,
        'name': lunch_ticket.user.get_full_name() if lunch_ticket.user else lunch_ticket.company.name,
        'email_address': lunch_ticket.user.email if lunch_ticket.user else lunch_ticket.email_address,
        'comment': lunch_ticket.comment,
        'date': lunch_ticket.time.__str__() if lunch_ticket.time else lunch_ticket.day.__str__(),
        'used': lunch_ticket.used,
        'type': lunch_ticket.get_ticket_type(),
        'token': lunch_ticket.token,
		'dietary_restrictions': [dietary_restriction.name for dietary_restriction in lunch_ticket.dietary_restrictions.all()],
		'other_dietary_restrictions': lunch_ticket.other_dietary_restrictions,
    }

    return data


def banquet_participant(banquet_participant):
    data = {
        'id': banquet_participant.pk,
        'token': str(banquet_participant.token),
        'title': banquet_participant.banquet.name
    }

    return data
