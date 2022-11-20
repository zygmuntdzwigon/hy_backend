from rest_framework import generics
from .models import Event, Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EventListSerializer, EventCreateSerializer, EventDetailsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from collections import OrderedDict

class EventsPaginator(LimitOffsetPagination):
    last_page_number = None

    def paginate_queryset(self, queryset, request, view=None):
        self.last_page_number = int(queryset.count() / self.get_limit(request))
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('lastPage', self.last_page_number)
        ]))

class EventsListView(generics.ListAPIView):
    serializer_class = EventListSerializer
    pagination_class = EventsPaginator

    def get_queryset(self):
        events = Event.objects.all()

        name_query = self.request.query_params.get('name')
        if name_query:
            events = events.filter(name__contains=name_query)

        city_query = self.request.query_params.get('city')
        if city_query:
            events = events.filter(city__contains=city_query)

        from_query = self.request.query_params.get('dateFrom')
        if from_query:
            events = events.filter(date_from__gt=from_query)

        to_query = self.request.query_params.get('dateTo')
        if to_query:
            events = events.filter(date_to__gt=to_query)

        tags_query = self.request.query_params.get('tags')
        if tags_query:
            events = events.filter(products__tag__in=tags_query)

        return events


class EventCreateView(generics.CreateAPIView):
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventDetailsSerializer
    queryset = Event.objects.all()


@api_view(['GET'])
def get_cities(request):
    cities = Event.objects.values_list('city', flat=True).distinct()
    return Response(data=cities)
