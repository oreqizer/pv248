create table if not exists book ( id integer not null primary key, name text not null, unique( name ) );
create table if not exists author ( id integer not null primary key, name text not null, unique( name ) );
create table if not exists book_author_list ( book_id integer references book( id ),
                                author_id integer references author( id ) );
