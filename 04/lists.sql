create table if not exists shopping_list ( id integer not null primary key,
                                           "date" date not null );

create table if not exists item ( id integer not null primary key,
                                  name text not null );

create table if not exists vendor ( id integer not null primary key,
                                    name text not null );

create table if not exists shop_list_item ( list_id integer not null references shopping_list( id ),
                                            item_id integer not null references item ( id ),
                                            quantity integer not null,
                                            vendor_id integer references vendor( id ),
                                            quantity_bought integer );

create table if not exists supplies ( item_id integer references item( id ),
                                      quantity integer not null,
                                      minimal integer not null,
                                      preferred integer not null );

create table if not exists pricing ( vendor_id integer references vendor( id ),
                                     item_id integer references item( id ),
                                     price integer,
                                     start_date date not null,
                                     unique( vendor_id, item_id, start_date ) );

