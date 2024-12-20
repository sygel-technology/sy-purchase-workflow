import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-sygel-technology-sy-purchase-workflow",
    description="Meta package for sygel-technology-sy-purchase-workflow Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-purchase_order_archive_draft>=16.0dev,<16.1dev',
        'odoo-addon-purchase_split_wizard>=16.0dev,<16.1dev',
        'odoo-addon-purchase_split_wizard_deposit>=16.0dev,<16.1dev',
        'odoo-addon-purchase_split_wizard_order_type>=16.0dev,<16.1dev',
        'odoo-addon-purchase_split_wizard_stock>=16.0dev,<16.1dev',
        'odoo-addon-vendor_pricelist_category>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
