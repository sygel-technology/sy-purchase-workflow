import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-sygel-technology-sy-purchase-workflow",
    description="Meta package for sygel-technology-sy-purchase-workflow Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-purchase_internal_product_reference>=15.0dev,<15.1dev',
        'odoo-addon-purchase_order_line_display_number>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
