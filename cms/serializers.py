from datetime import datetime, timezone
from rest_framework.serializers import (Serializer,
                                        BooleanField,
                                        IntegerField,
                                        SerializerMethodField,
                                        UUIDField)


class ListPaginationSerializer(Serializer):
    next = IntegerField()
    previous = IntegerField()
    current = IntegerField()
    pages = IntegerField()
    count = IntegerField()


class StepListBaseSerializer(Serializer):
    title = SerializerMethodField()
    uuid = UUIDField()
    created = SerializerMethodField()
    updated = SerializerMethodField()

    APP_TIME_FORMAT = '%Y-%m-%d %H:%M'
    API_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
    
    def get_title(self, obj):
        return obj['title'] or '-'
        
    def get_created(self, obj):
        return self.convert_datetime(obj['created'])

    def get_updated(self, obj):
        return self.convert_datetime(obj['updated'])

    def convert_datetime(self, to_convert):
        dt = datetime.strptime(to_convert, self.API_TIME_FORMAT) \
                    .replace(tzinfo=timezone.utc)
        return dt.strftime(self.APP_TIME_FORMAT)


class SequenceSerializer(StepListBaseSerializer):
    is_published = SerializerMethodField()
    published = SerializerMethodField()

    def get_is_published(self, obj):
        published = obj['published']
        
        if published is not None:
            return self.convert_datetime(published)
        else:
            return None

    def get_published(self, obj):
        published = obj['published']
        if published is not None:
            return self.convert_datetime(published)
        return None

    def convert_datetime(self, to_convert):
        dt = datetime.strptime(to_convert, self.API_TIME_FORMAT) \
                    .replace(tzinfo=timezone.utc)
        return dt.strftime(self.APP_TIME_FORMAT)


class SequencesSerializer(ListPaginationSerializer):
    sequences = SequenceSerializer(many=True, source='results')


class StepsSerializer(ListPaginationSerializer):
    steps = StepListBaseSerializer(many=True, source='results')
    
    
class StepSerializer(StepListBaseSerializer):
    linked = StepListBaseSerializer(many=True)