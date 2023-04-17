**ProductInvetory** ekleme ekranında `product_type` işaretleniyor
`product_type` FK -> **ProductType**

Örnek:
Dropdown: `product_type == 'Televizyon'` seçersek;

**ProductTypeAttribute** içerisinde `product_type` fieldı `Televizyon` olan nesneleri çekiyoruz ve bunların `product_attribute`(FK)  değerlerini gösteriyoruz.

Örnek:
Dropdown: `product_attribute == 'Ekran Boyutu'` seçersek:
**ProductAttributeValue** içerisinden `product_attribute` fieldı `Ekran Boyutu` olan nesneleri çekiyoruz ve bunların `attribute_value` değerlerini gösteriyoruz.


Dropdown 1 (`product_type`): Televizyon
Dropdown 2 (`product_attribute`): Ekran Boyutu
Dropdown 3 (`attribute_value`): 24" / 61 Ekran