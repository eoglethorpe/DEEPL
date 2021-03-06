from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from clustering.models import ClusteringModel
from clustering.serializers import ClusteringModelSerializer
from clustering.tasks import create_new_clusters
from classifier.models import ClassifiedDocument


import logging
logger = logging.getLogger(__name__)


class ClusteringView(APIView):
    """
    API for document clusters
    """
    def get(self, request, version=None):
        data = dict(request.query_params.items())
        validation_details = self._validate_get_data(data)
        if not validation_details['status']:
            return Response(
                validation_details['errors'],
                status=status.HTTP_400_BAD_REQUEST
            )
        model_id = data['model_id']
        try:
            cluster_model = ClusteringModel.objects.get(id=model_id)
        except ClusteringModel.DoesNotExist:
            return Response(
                {'message': 'Clustering model corresponding to model id does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ClusteringModelSerializer(cluster_model)
        return Response(serializer.data)

    def post(self, request, version=None):
        data = dict(request.data.items())
        validation_details = self._validate_post_data(data)
        if not validation_details['status']:
            return Response(
                validation_details['errors'],
                status=status.HTTP_400_BAD_REQUEST
            )
        grp_id = data['group_id']
        num_clusters = int(data['num_clusters'])
        # first try get if any docs available with given group_id

        docs = ClassifiedDocument.objects.filter(group_id=grp_id)
        if not docs or docs.count() <= num_clusters:
            return Response(
                {'message': 'Too few/zero documents to cluster'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            cluster_model = ClusteringModel.objects.get(
                group_id=grp_id
            )
        except ClusteringModel.DoesNotExist:
            # TODO: find optimal clusters
            cluster_model = create_new_clusters.delay(
                data.get('name', grp_id),  # name is not mandatory
                grp_id,
                n_clusters=num_clusters,
            )
            return Response(
                {"message": "Clustering is in progress. Try later for data."},
                status=status.HTTP_202_ACCEPTED
            )
        if not cluster_model.ready:
            return Response(
                {"message": "Clustering is in progress. Try later for data."},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            {'cluster_id': cluster_model.id},
            status=status.HTTP_201_CREATED
        )

    def _validate_post_data(self, data):
        errors = {}
        if not data.get('group_id'):
            errors['group_id'] = 'Group id should be present'
        num_clusters = data.get('num_clusters')
        try:
            n = int(num_clusters)
            if n < 0:
                raise ValueError
        except (ValueError, TypeError):
            errors['num_clusters'] = 'num_clusters should be an integer'
        if errors:
            return {
                'status': False,
                'errors': errors
            }
        return {
            'status': True,
            'data': data
        }

    def _validate_get_data(self, data):
        errors = {}
        model_id = data.get('model_id')
        if not model_id:
            errors['model_id'] = "Cluster model_id should be present"
        else:
            try:
                i = int(model_id)
                if i < 0:
                    raise ValueError
            except (ValueError, TypeError):
                errors['model_id'] = 'model_id should be positive integer'
        if errors:
            return {
                'status': False,
                'errors': errors
            }
        return {
            'status': True,
            'data': data
        }
