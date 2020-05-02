from django import forms
from cities.models import City
from routes.models import Route


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Звідки', queryset=City.objects.all(),
                            widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}))
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                            widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}))
    cities = forms.ModelMultipleChoiceField(label='Через міста', queryset=City.objects.all(),
                            required=False,
                            widget=forms.SelectMultiple(attrs={'class': 'form-control js-example-basic-multiple'}))
    travelling_time = forms.IntegerField(label='Потяг', widget=forms.NumberInput(
                                attrs={'class': 'form-control',
                                       'placeholder': 'Час в дорозі'}))


class RouteModelForm(forms.ModelForm):
    name = forms.CharField(label='Назва маршруту',
            widget=forms.TextInput(attrs={'class': 'form-control'}))
    from_city = forms.CharField(widget=forms.HiddenInput())
    to_city = forms.CharField(widget=forms.HiddenInput())
    trains = forms.CharField(widget=forms.HiddenInput())
    travel_times = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Route
        fields = ('name', 'from_city', 'to_city', 'trains', 'travel_times')