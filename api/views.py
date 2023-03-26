from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Event
from .serializers import EventListSerializer, EventCreateSerializer, EventDetailsSerializer


class EventsListView(generics.ListAPIView):
    serializer_class = EventListSerializer

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


class EventCreateView(generics.ListCreateAPIView):
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj: Event):
        return request.user == obj.owner


class EventDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventDetailsSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        Event.objects.get(id=self.kwargs['pk'])

@api_view(['POST'])
def add_event_banner(request: Request, pk: int):
    banner = request.FILES['banner']
    if banner:
        event = Event.objects.get(id=pk)
        if event.owner != request.user:
            return Response(200)
        if event:
            event.banner = banner
            return Response(200)
        return Response(404)
    return Response(400)


@api_view(['GET'])
def get_cities(request):
    cities = Event.objects.values_list('city', flat=True).distinct()
    return Response(data=cities)
