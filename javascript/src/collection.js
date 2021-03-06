/**
 * @fileoverview Base class for ImageCollection and FeatureCollection.
 * This class is never intended to be instantiated by the user.
 *
 */

goog.provide('ee.Collection');

goog.require('ee.ApiFunction');
goog.require('ee.Element');
goog.require('ee.Filter');



/**
 * Constructs a base collection by passing the representaion up to Element.
 * @param {ee.Function} func The same argument as in ee.ComputedObject().
 * @param {Object} args The same argument as in ee.ComputedObject().
 * @param {string?=} opt_varName The same argument as in ee.ComputedObject().
 * @constructor
 * @extends {ee.Element}
 */
ee.Collection = function(func, args, opt_varName) {
  goog.base(this, func, args, opt_varName);
  ee.Collection.initialize();
};
goog.inherits(ee.Collection, ee.Element);
// Exporting manually to avoid marking the class public in the docs.
goog.exportSymbol('ee.Collection', ee.Collection);


/**
 * Whether the class has been initialized with API functions.
 * @type {boolean}
 * @private
 */
ee.Collection.initialized_ = false;


/**
 * Imports API functions to this class.
 */
ee.Collection.initialize = function() {
  if (!ee.Collection.initialized_) {
    ee.ApiFunction.importApi(ee.Collection, 'Collection', 'Collection');
    ee.ApiFunction.importApi(ee.Collection,
                             'AggregateFeatureCollection',
                             'Collection',
                             'aggregate_');
    ee.Collection.initialized_ = true;
  }
};


/**
 * Removes imported API functions from this class and resets the serial ID
 * used for mapping JS functions to 0.
 */
ee.Collection.reset = function() {
  ee.ApiFunction.clearApi(ee.Collection);
  ee.Collection.initialized_ = false;
};


/**
 * Apply a filter to this collection.
 *
 * Collection filtering is done by wrapping a collection in a filter
 * algorithm.  As additional filters are applied to a collection, we
 * try to avoid adding more wrappers and instead search for a wrapper
 * we can add to, however if the collection doesn't have a filter, this
 * will wrap it in one.
 *
 * @param {ee.Filter} newFilter - A filter to add to this collection.
 * @return {ee.Collection} The filtered collection.
 * @export
 */
ee.Collection.prototype.filter = function(newFilter) {
  if (!newFilter) {
    throw new Error('Empty filters.');
  }
  return this.castInternal(ee.ApiFunction._call(
      'Collection.filter', this, newFilter));
};


/**
 * Shortcuts to filter a collection by metadata.  This is equivalent
 * to this.filter(ee.Filter.metadata(...)).
 *
 * @param {string} name The name of a property to filter.
 * @param {string} operator The name of a comparison operator.
 *     Possible values are: "equals", "less_than", "greater_than",
 *     "not_equals", "not_less_than", "not_greater_than", "starts_with",
 *     "ends_with", "not_starts_with", "not_ends_with", "contains",
 *     "not_contains".
 * @param {*} value - The value to compare against.
 * @return {ee.Collection} The filtered collection.
 * @export
 * @suppress {deprecated} We get to use this for now.
 * TODO(user): Decide whether to deprecate this.
 */
ee.Collection.prototype.filterMetadata = function(name, operator, value) {
  return this.filter(ee.Filter.metadata(name, operator, value));
};


/**
 * Shortcut to filter a collection by geometry.  Items in the
 * collection with a footprint that fails to intersect the bounds
 * will be excluded when the collection is evaluated.
 *
 * This is equivalent to this.filter(ee.Filter.bounds(...)).
 * @param {ee.Feature|ee.Geometry} geometry The geometry to filter to.
 * @return {ee.Collection} The filtered collection.
 * @export
 */
ee.Collection.prototype.filterBounds = function(geometry) {
  return this.filter(ee.Filter.bounds(geometry));
};


/**
 * Shortcut to filter a collection by a date range.  Items in the
 * collection with a time_start property that doesn't fall between the
 * start and end dates will be excluded.
 *
 * This is equivalent to this.filter(ee.Filter.date(...)).
 *
 * @param {Date|string|number} start The start date as a Date object,
 *     a string representation of a date, or milliseconds since epoch.
 * @param {Date|string|number=} opt_end The end date as a Date object,
 *     a string representation of a date, or milliseconds since epoch.
 * @return {ee.Collection} The filtered collection.
 * @export
 */
ee.Collection.prototype.filterDate = function(start, opt_end) {
  return this.filter(ee.Filter.date(start, opt_end));
};


/**
 * Limit a collection to the specified number of elements, optionally
 * sorting them by a specified property first.
 *
 * @param {number} max - The number to limit the collection to.
 * @param {string=} opt_property - The property to sort by, if sorting.
 * @param {boolean=} opt_ascending - Whether to sort in ascending or
 *     descending order.  The default is true (ascending).
 * @return {ee.Collection} The limited collection.
 * @export
 */
ee.Collection.prototype.limit = function(max, opt_property, opt_ascending) {
  return this.castInternal(ee.ApiFunction._call(
      'Collection.limit', this, max, opt_property, opt_ascending));
};


/**
 * Sort a collection by the specified property.
 *
 * @param {string} property - The property to sort by.
 * @param {boolean=} opt_ascending - Whether to sort in ascending or descending
 *     order.  The default is true (ascending).
 * @return {ee.Collection} The sorted collection.
 * @export
 */
ee.Collection.prototype.sort = function(property, opt_ascending) {
  return this.castInternal(ee.ApiFunction._call(
      'Collection.limit', this, undefined, property, opt_ascending));
};


/** @override */
ee.Collection.prototype.name = function() {
  return 'Collection';
};


/**
 * Returns the type constructor of the collection's elements.
 * @return {function(new:Object, ...?)}
 * @protected
 */
ee.Collection.prototype.elementType = function() {
  return ee.Element;
};


/**
 * Maps an algorithm over a collection.
 *
 * @param {function(Object):Object} algorithm The operation to map over
 *     the images or features of the collection. A JavaScript function that
 *     receives an image or features and returns one. The function is called
 *     only once and the result is captured as a description, so it cannot
 *     perform imperative operations or rely on external state.
 * @param {boolean=} opt_dropNulls If true, the mapped algorithm is allowed
 *     to return nulls, and the elements for which it returns nulls will be
 *     dropped.
 * @return {ee.Collection} The mapped collection.
 * @export
 */
ee.Collection.prototype.map = function(algorithm, opt_dropNulls) {
  var elementType = this.elementType();
  var withCast = function(e) { return algorithm(new elementType(e)); };
  return this.castInternal(ee.ApiFunction._call(
      'Collection.map', this, withCast, opt_dropNulls));
};


/**
 * Applies a user-supplied function to each element of a collection. The
 * user-supplied function is given two arguments: the current element, and
 * the value returned by the previous call to iterate() or the first argument,
 * for the first iteration. The result is the value returned by the final
 * call to the user-supplied function.
 *
 * @param {function(Object, Object):Object} algorithm The function to apply
 *     to each element. Must take two arguments: an element of the collection
 *     and the value from the previous iteration.
 * @param {*=} opt_first The initial state.
 * @return {ee.ComputedObject} The result of the Collection.iterate() call.
 * @export
 */
ee.Collection.prototype.iterate = function(algorithm, opt_first) {
  var first = goog.isDef(opt_first) ? opt_first : null;
  var elementType = this.elementType();
  var withCast = function(e, p) { return algorithm(new elementType(e), p); };
  return ee.ApiFunction._call('Collection.iterate', this, withCast, first);
};
