from django.template import Library

from comp.models import Registration, Submission

register = Library()


@register.filter
def comp_all(comp):
    return Registration.objects.filter(comp=comp).count()


@register.filter
def rank(comp, user):
    max_score = Submission.objects.filter(user=user).order_by('score').last()
    print(max_score)
    return Submission.objects.filter(comp=comp).filter(score__gt=max_score.score).count() + 1


register.filter('comp_all', comp_all)
register.filter('rank', rank)
