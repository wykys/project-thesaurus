from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateTimeField, CurrentUserDefault, HiddenField
from rest_framework.relations import PrimaryKeyRelatedField, HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer

from apps.accounts.serializers import UserSerializer
from apps.review.models import Review
from apps.thesis.models import Thesis


class ReviewPublicSerializer(ModelSerializer):
    thesis = PrimaryKeyRelatedField(
        queryset=Thesis.objects.get_queryset(),
        style=dict(base_template='input.html'),
    )
    user = UserSerializer(read_only=True)
    user_id = HiddenField(default=CurrentUserDefault(), source='user', write_only=True)

    url = HyperlinkedIdentityField(view_name='api:review-pdf-detail')

    created = DateTimeField(read_only=True, format=None)

    class Meta:
        model = Review
        fields = (
            'id',
            'url',
            'thesis',
            'user',
            'user_id',
            'difficulty',
            'grades',
            'grade_proposal',
            'created',
        )

    def validate(self, attrs):
        thesis = attrs.get('thesis')
        user = self.context.get('request').user if not self.instance else self.instance.user

        if not (
                thesis.state == Thesis.State.READY_FOR_REVIEW and
                user in (thesis.supervisor, thesis.opponent) and
                not Review.objects.filter(
                    thesis=thesis,
                    user=user
                ).exclude(
                    id=self.instance.id if self.instance else None
                ).exists()
        ):
            raise ValidationError(_('Review has been already posted by this user or this user is not allowed to post '
                                    'review for this thesis.'))

        return attrs


class ReviewFullInternalSerializer(ReviewPublicSerializer):
    class Meta(ReviewPublicSerializer.Meta):
        fields = ReviewPublicSerializer.Meta.fields + (
            'comment',
            'questions',
        )
