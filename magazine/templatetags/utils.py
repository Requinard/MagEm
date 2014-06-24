from django import template

register = template.Library()


@register.filter(name="get_score")
def get_score(value, scores):
	return scores[value]