import uuid
import base64
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

class BaseModel(models.Model):
    """BaseModel for all other models"""
    idx = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(editable=False)
    modified_on = models.DateTimeField()

    def save(self, *args, **kwargs):
        """Override to upate created_on and modified_on"""
        if not self.id:
            self.created_on = timezone.now()
        self.modified_on = timezone.now()
        return super().save( *args, **kwargs)

class ClassifierModel(BaseModel):
    """
    Model to store classifier specific data.
    This stores pickled data as text
    """
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20, unique=True, editable=False)
    # _data is for storing the pickled classifier object
    _data = models.TextField(db_column='data')
    accuracy = models.FloatField(default=0)
    description = models.TextField()

    def set_data(self, data):
        self._data = base64.b64encode(data)
    def get_data(self):
        return base64.b64decode(self._data)

    data = property(get_data, set_data)

    def __str__(self):
        return 'v{}-{}'.format(self.version, self.name)


class ClassifiedDocument(BaseModel):
    """
    Model to store the classified document details(especially for deeper
    """
    classifier = models.ForeignKey(ClassifierModel)
    group_id = models.CharField(max_length=20)
    classification = models.CharField(max_length=50)
    confidence = models.FloatField(default=0)
    classification_probabilities = JSONField(default=[])
    text = models.TextField()
    details = models.TextField()

    def __str__(self):
        return '{} {}'.format(group_id, classification)


class ClassifiedExcerpt(BaseModel):
    """
    Model to store classified excerpts from the documents
    """
    classified_document = models.ForeignKey(ClassifiedDocument, related_name="excerpts")
    start_pos = models.IntegerField()
    end_pos = models.IntegerField()
    classification = models.CharField(max_length=50)
    confidence = models.FloatField(default=0)
    classification_probabilities = JSONField(default=[])

    def __str__(self):
        return '{} - {} : {}'.format(start_pos, end_pos, classification)
