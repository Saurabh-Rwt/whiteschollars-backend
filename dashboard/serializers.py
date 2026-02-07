from rest_framework import serializers
from .models import (
    Course, Section, KeyHighlight, AccreditationsAndCertification,
    WhyChoose, Mentor, ProgramHighlight, CareerAssistance,
    CareerTransition, OurAlumni, OnCampusClass,
    FeeStructure, ProgramFor, WhyWhiteScholars, ListenOurExpert
)

# ----------------- Basic Serializers -----------------

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class KeyHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyHighlight
        fields = '__all__'

class AccreditationsAndCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccreditationsAndCertification
        fields = '__all__'

class WhyChooseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyChoose
        fields = '__all__'

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'

class ProgramHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramHighlight
        fields = '__all__'

class CareerAssistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerAssistance
        fields = '__all__'

class CareerTransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerTransition
        fields = '__all__'

class OurAlumniSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurAlumni
        fields = '__all__'

class OnCampusClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnCampusClass
        fields = '__all__'

class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'

class ProgramForSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramFor
        fields = '__all__'

class WhyWhiteScholarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyWhiteScholars
        fields = '__all__'

class ListenOurExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListenOurExpert
        fields = '__all__'

# ----------------- Course Serializers -----------------

class CourseSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        source='meta_description',
        allow_blank=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'slug', 'description', 'created_at']


# ----------------- Full Course Detail Serializer -----------------

class CourseFullDetailSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        source='meta_description',
        allow_blank=True,
        allow_null=True,
        required=False
    )
    sections = SectionSerializer(many=True, read_only=True)
    key_highlights = KeyHighlightSerializer(many=True, read_only=True)
    accreditations_certifications = AccreditationsAndCertificationSerializer(many=True, read_only=True)
    why_choose_items = WhyChooseSerializer(many=True, read_only=True)
    mentors = MentorSerializer(many=True, read_only=True)
    program_highlights = ProgramHighlightSerializer(many=True, read_only=True)
    career_assistances = CareerAssistanceSerializer(many=True, read_only=True)
    career_transitions = CareerTransitionSerializer(many=True, read_only=True)
    our_alumni = OurAlumniSerializer(many=True, read_only=True)
    on_campus_classes = OnCampusClassSerializer(many=True, read_only=True)
    fee_structures = FeeStructureSerializer(many=True, read_only=True)
    program_for = ProgramForSerializer(many=True, read_only=True)
    why_white_scholars = WhyWhiteScholarsSerializer(many=True, read_only=True)
    listen_our_experts = ListenOurExpertSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'slug', 'description',
            'sections', 'key_highlights', 'accreditations_certifications',
            'why_choose_items', 'mentors', 'program_highlights',
            'career_assistances', 'career_transitions', 'our_alumni',
            'on_campus_classes', 'fee_structures', 'program_for',
            'why_white_scholars', 'listen_our_experts'
        ]
