import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-sygel-technology-sy-purchase-workflow",
    description="Meta package for sygel-technology-sy-purchase-workflow Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-stock_rule_mto_vendor_purchase_type',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)
