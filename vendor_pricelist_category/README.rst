.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
  :target: http://www.gnu.org/licenses/agpl
  :alt: License: AGPL-3

=========================
Vendor Pricelist Category
=========================

This module allows to select a category in vendor pricelists and choose whether these categories have to apply a discount when the pricelists are selected in a purchase order.


Installation
============

To install this module, you need to:

#. Only install


Configuration
=============

To create new vendor pricelists categories, you need to:

#. Go to Purchase > Configuration > Vendor Pricelist Categories.
#. Select a name, a code and a vendor which can appy this category.
#. Select a parent category if necessary.
#. Check the "Use Discount in Supplierinfo" if this category applies a discount.
#. Check the "Use Different Parent Discount" if the disccount applied by this category can be different from the discount applied in it parent category (if a parent category has been selected).

To assign a category to a vendor pricelist, you need to:

#. Go to Purchase > Configuration > Vendor Pricelists.
#. Go to a Vendor Pricelist and select a Category in the "Category" field. Only categories related to the pricelist's partner can be selected.


Usage
=====

To use this module, you need to:

#. Create a purchase and select a vendor pricelist with a category.
#. If the category applies a discount, this discount will be shown in the Discount field in the purchase order lines.


Bug Tracker
===========

Bugs and errors are managed in `issues of GitHub <https://github.com/sygel-technology/sy-purchase-workflow/issues>`_.
In case of problems, please check if your problem has already been
reported. If you are the first to discover it, help us solving it by indicating
a detailed description `here <https://github.com/sygel-technology/sy-purchase-workflow/issues/new>`_.

Do not contact contributors directly about support or help with technical issues.


Credits
=======

Authors
~~~~~~~

* Sygel, Odoo Community Association (OCA)


Contributors
~~~~~~~~~~~~

* Manuel Regidor <manuel.regidor@sygel.es>


Maintainer
~~~~~~~~~~

This module is maintained by Sygel.

.. image:: https://www.sygel.es/logo.png
   :alt: Sygel
   :target: https://www.sygel.es

This module is part of the `sygel-technology/sy-purchase-workflow <https://github.com/sygel-technology/sy-purchase-workflow>`_.

To contribute to this module, please visit https://github.com/sygel-technology.
