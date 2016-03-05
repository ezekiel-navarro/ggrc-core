# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: laran@reciprocitylabs.com
# Maintained By: laran@reciprocitylabs.com

from ggrc import db
from ggrc.models.mixins import Base


class CustomAttributeValue(Base, db.Model):
  __tablename__ = 'custom_attribute_values'

  custom_attribute_id = db.Column(
      db.Integer,
      db.ForeignKey('custom_attribute_definitions.id', ondelete="CASCADE")
  )
  attributable_id = db.Column(db.Integer)
  attributable_type = db.Column(db.String)
  attribute_value = db.Column(db.String)
  attribute_object_id = db.Column(db.Integer)

  @property
  def attributable_attr(self):
    return '{0}_attributable'.format(self.attributable_type)

  @property
  def attributable(self):
    return getattr(self, self.attributable_attr)

  @attributable.setter
  def attributable(self, value):
    self.attributable_id = value.id if value is not None else None
    self.attributable_type = value.__class__.__name__ if value is not None \
        else None
    return setattr(self, self.attributable_attr, value)

  _publish_attrs = [
      'custom_attribute_id',
      'attributable_id',
      'attributable_type',
      'attribute_value',
      'attribute_object',
  ]

  @property
  def attribute_object(self):
    return getattr(self, self._attribute_object_attr)

  @attribute_object.setter
  def attribute_object(self, value):
    self.attribute_object_id = value.id
    return setattr(self, self._attribute_object_attr, value)

  @property
  def attribute_object_type(self):
    """Fetch the mapped object pointed to by attribute_object_id.

    Returns:
       A model of type referenced in attribute_value
    """
    attr_type = self.custom_attribute.attribute_type
    if not attr_type.startswith("Map:"):
      return None
    return self.attribute_object.__class__.__name__

  @property
  def _attribute_object_attr(self):
    """Compute the relationship property based on object type.

    Returns:
        Property name
    """
    attr_type = self.custom_attribute.attribute_type
    if not attr_type.startswith("Map:"):
      return None
    return 'attribute_{0}'.format(self.attribute_value)

  @classmethod
  def mk_filter_by_custom(cls, obj_class, custom_attribute_id):
    def filter_by(predicate):
      return cls.query.filter(
          (cls.custom_attribute_id == custom_attribute_id) &
          (cls.attributable_type == obj_class.__name__) &
          (cls.attributable_id == obj_class.id) &
          predicate(cls.attribute_value)
      ).exists()
    return filter_by
