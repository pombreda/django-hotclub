from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from friends.forms import InviteFriendForm
from friends.models import FriendshipInvitation, Friendship

from zwitschern.models import Following

from profiles.models import Profile
from profiles.forms import ProfileForm

try:
    from notification import models as notification
except ImportError:
    notification = None

def profiles(request):
    return render_to_response("profiles/profiles.html", {
        "users": User.objects.all().order_by("-date_joined"),
    }, context_instance=RequestContext(request))

def profile(request, username):
    other_user = get_object_or_404(User, username=username)
    if request.user.is_authenticated():
        is_friend = Friendship.objects.are_friends(request.user, other_user)
        is_following = Following.objects.is_following(request.user, other_user)
        other_friends = Friendship.objects.friends_for_user(other_user)
        if request.user == other_user:
            is_me = True
        else:
            is_me = False
    else:
        other_friends = []
        is_friend = False
        is_me = False
        is_following = False
    
    if request.user.is_authenticated() and request.method == "POST" and not is_me:
        
        # @@@ some of this should go in zwitschern itself
        
        if request.POST["action"] == "follow":
            Following.objects.follow(request.user, other_user)
            is_following = True
            request.user.message_set.create(message=_("You are now following %(other_user)s") % {'other_user': other_user})
            if notification:
                notification.send([other_user], "tweet_follow", "%s is now following your tweets", [request.user])
        elif request.POST["action"] == "unfollow":
            Following.objects.unfollow(request.user, other_user)
            is_following = False
            request.user.message_set.create(message=_("You have stopped following %(other_user)s") % {'other_user': other_user})
    
    if is_friend:
        invite_form = None
        previous_invitations_to = None
        previous_invitations_from = None
    else:
        if request.user.is_authenticated() and request.method == "POST":
            if request.POST["action"] == "invite":
                invite_form = InviteFriendForm(request.user, request.POST)
                if invite_form.is_valid():
                    invite_form.save()
            else:
                invite_form = InviteFriendForm(request.user, {
                    'to_user': username,
                })
                if request.POST["action"] == "accept": # @@@ perhaps the form should just post to friends and be redirected here
                    invitation_id = request.POST["invitation"]
                    try:
                        invitation = FriendshipInvitation.objects.get(id=invitation_id)
                        if invitation.to_user == request.user:
                            invitation.accept()
                            request.user.message_set.create(message=_("You have accepted the friendship request from %(from_user)s") % {'from_user': invitation.from_user})
                            is_friend = True
                            other_friends = Friendship.objects.friends_for_user(other_user)
                    except FriendshipInvitation.DoesNotExist:
                        pass
        else:
            invite_form = InviteFriendForm(request.user, {
                'to_user': username,
                'message': ugettext("Let's be friends!"),
            })
    previous_invitations_to = FriendshipInvitation.objects.filter(to_user=other_user, from_user=request.user)
    previous_invitations_from = FriendshipInvitation.objects.filter(to_user=request.user, from_user=other_user)
    
    if is_me:
        if request.method == "POST":
            if request.POST["action"] == "update":
                profile_form = ProfileForm(request.POST, instance=other_user.get_profile())
                profile = profile_form.save(commit=False)
                profile.user = other_user
                profile.save()
        try:
            profile_form = ProfileForm(instance=other_user.get_profile())
        except Profile.DoesNotExist:
            profile = Profile(user=other_user)
            profile.save()
            profile_form = ProfileForm(instance=other_user.get_profile())
    else:
        profile_form = None
    
    return render_to_response("profiles/profile.html", {
        "profile_form": profile_form,
        "is_me": is_me,
        "is_friend": is_friend,
        "is_following": is_following,
        "other_user": other_user,
        "other_friends": other_friends,
        "invite_form": invite_form,
        "previous_invitations_to": previous_invitations_to,
        "previous_invitations_from": previous_invitations_from,
    }, context_instance=RequestContext(request))