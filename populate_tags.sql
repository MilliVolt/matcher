do $$
    declare 
        tag_name text;
    begin
        for tag_name in
            select unnest(tags) from tft.video
        loop
            insert into tft.tags (tag) values (tag_name)
            on conflict do nothing;
        end loop;
    end; 
$$
