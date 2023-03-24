import logging

from .registry import class_name, SERIALIZERS

logger = logging.getLogger(__name__)

# Keep track of which warnings have been printed
NO_SERIALIZER_FOR_INSTANCE = {}


def serialize(parent, instance, instance_id, context, depth):
    instance_type = class_name(instance)
    serializer = SERIALIZERS[instance_type] if instance_type in SERIALIZERS else None

    if serializer:
        return serializer(parent, instance, instance_id, context, depth)

    if instance_type not in NO_SERIALIZER_FOR_INSTANCE:
        # Only print the warning once for each type of serializer
        logger.warning(f"!!!No serializer for {instance_type} with id {instance_id}")
        NO_SERIALIZER_FOR_INSTANCE[instance_type] = instance_id

    return None


def serialize_widget(dict_out, widget):
    instance_type = class_name(widget)
    logger.debug(f"Widget serialization {instance_type}")
