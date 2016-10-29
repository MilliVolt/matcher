do $$
declare
begin
    create table temp (
        vid uuid,
        vtag text);

    insert into temp
    select 
        id as vid, 
        unnest(tags) as vtag 
    from tft.video; 

    insert into tft.videotags (
        select uuid_generate_v4() as id,
            vid as video_id,
            id as tag_id
        from temp
        left join
            tft.tags
        on (temp.vtag = tft.tags.tag)
    );
    drop table temp;
end;
$$
