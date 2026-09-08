from django import template

register = template.Library()

@register.filter
def is_agent(user):
    try:
        return user.profile.role == 'Agent'
    except Exception:
        return False
