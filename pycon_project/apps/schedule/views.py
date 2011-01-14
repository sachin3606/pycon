from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from proposals.models import Proposal
from review.models import ProposalResult
from schedule.models import Slot, Session


def schedule_list(request, template_name="schedule/schedule_list.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    slots = Slot.objects.all().order_by("start")
    
    return render_to_response(template_name, dict({
        "slots": slots,
        "timezone": settings.SCHEDULE_TIMEZONE,
    }, **extra_context), context_instance=RequestContext(request))


def schedule_session(request, session_id, template_name="schedule/session_detail.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    session = Session.objects.get(id=session_id)
    
    return render_to_response(template_name, dict({
        "session": session,
        "timezone": settings.SCHEDULE_TIMEZONE,
    }, **extra_context), context_instance=RequestContext(request))


def tmp_schedule_session(request, proposal_id):
    
    proposal = get_object_or_404(Proposal, pk=proposal_id, result__accepted=True)
    
    return render_to_response("schedule/tmp_session_detail.html", {
        "proposal": proposal
    }, context_instance=RequestContext(request))


def schedule_list_talks(request):
    
    talks = ProposalResult.objects.filter(
        accepted=True,
        proposal__session_type__in=[Proposal.SESSION_TYPE_PANEL, Proposal.SESSION_TYPE_TALK]
    ).select_related("proposal", "proposal__speaker")
    
    return render_to_response("schedule/list_talks.html", dict({
        "talks": talks,
    }), context_instance=RequestContext(request))


def schedule_list_tutorials(request):
    
    tutorials = ProposalResult.objects.filter(
        accepted=True,
        proposal__session_type=Proposal.SESSION_TYPE_TUTORIAL
    )
    
    return render_to_response("schedule/list_tutorials.html", dict({
        "tutorials": tutorials,
    }), context_instance=RequestContext(request))

    