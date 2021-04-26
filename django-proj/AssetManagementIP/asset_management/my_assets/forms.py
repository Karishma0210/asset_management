from django import forms
from .models import Asset


class AssetCreateForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = (
            'name',
            'manufacturer',
            'category',
            'location',
            'purchase_date',
            'warranty',
            'last_repair',
            'asset_user',
            'physical_address',
            'digital_key',
            'status',
            'note'
        )

        widgets = {
            # "Asset Name",
            'name': forms.TextInput(attrs={
                'class': 'form-control'}),
            # "Manufacturer",
            'manufacturer': forms.Select(attrs={
                'class': 'form-control'}),
            # "Category",
            'category': forms.Select(attrs={
                'class': 'form-control'}),
            # "Location",
            'location': forms.TextInput(attrs={
                'class': 'form-control', }),
            # "Purchase Date",
            'purchase_date': forms.DateInput(attrs={
                'class': 'form-control'}),
            # "Warranty (months)",
            'warranty': forms.NumberInput(attrs={
                'class': 'form-control'}),
            # "Last Repair",
            'last_repair': forms.DateInput(attrs={
                'class': 'form-control'}),
            # "Current User",
            'asset_user': forms.Select(attrs={
                'class': 'form-control'}),
            # "Physical Address",
            'physical_address': forms.TextInput(
                attrs={'class': 'form-control'}),
            # "Digital Key",
            'digital_key': forms.TextInput(attrs={
                'class': 'form-control'}),
            # "Status",
            'status': forms.Select(attrs={
                'class': 'form-control'}),
            # "Comments",
            'note': forms.Textarea(attrs={'class': 'form-control'})
        }
