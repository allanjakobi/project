from rest_framework import serializers
from .models import Model, Rendipillid

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'

class RendipillidSerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.SerializerMethodField()
    mobile_image = serializers.SerializerMethodField()
    desktop_image = serializers.SerializerMethodField()

    keyboard = serializers.IntegerField(source='modelId.keyboard', read_only=True)  # Access keyboard from the related model
    allkeys = serializers.IntegerField(source='modelId.keys', read_only=True)  # Access keys from the related model
    rate = serializers.DecimalField(source='rate.rate', max_digits=10, decimal_places=2, read_only=True)  # Include rate from the related table

    keyboardmax = serializers.SerializerMethodField()  # Custom field for max keyboard value
    whitekeys = serializers.SerializerMethodField()  # Custom field for white keys count
    whitekeywidth = serializers.SerializerMethodField()  # New field for white key width calculation

    modelId = ModelSerializer()  # Embed ModelSerializer to show model details

    class Meta:
        model = Rendipillid
        fields = '__all__'  # Include all fields

    def get_thumbnail_image(self, obj):
        return f"/media/300/R{obj.instrumentId}.jpg"

    def get_mobile_image(self, obj):
        return f"/media/700/R{obj.instrumentId}.jpg"

    def get_desktop_image(self, obj):
        return f"/media/1200/R{obj.instrumentId}.jpg"
    
    def get_keyboardmax(self, obj):
        # Custom field: Increase the keyboard value by 3.3
        return round (obj.modelId.keyboard + 3.3, 2)
    
    def get_whitekeys(self, obj):
        # Extract keys and low from the related model
        keys = obj.modelId.keys
        low = obj.modelId.low
        
        # Call the white key calculation logic
        return self.calculate_white_keys(keys, low)

    def calculate_white_keys(self, keys, low):
        # Define the white/black key pattern
        pattern = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1] 
        offset = low % 12  # Calculate the starting offset in the pattern

        white_keys_count = 0
        i = 0  # Pattern index
        key_count = 0  # Counter for keys to ensure we don't exceed total keys

        # Loop through the pattern to count white keys
        while key_count < keys:
            shifted_i = (i + offset) % 12  # Calculate the current position in the pattern
            white_keys_count += pattern[shifted_i]  # Add 1 if it's a white key (pattern[i] == 1)
            i += 1
            key_count += 1
        
        return white_keys_count

    def get_whitekeywidth(self, obj):
        # Calculate whitekeywidth as keyboard / whitekeys
        keyboard = obj.modelId.keyboard
        whitekeys = self.get_whitekeys(obj)
        
        if whitekeys == 0:  # Prevent division by zero
            return None
        return round(keyboard / whitekeys, 2)
