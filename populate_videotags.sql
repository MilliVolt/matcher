do $$
    declare 
        vid uuid;
        tid uuid;
        vtag text;
    begin
       INSERT into tft.videotags (video_id) values (vid, tid)
       --join tft.tags on unnest(tft.video.tags) = tft.tags.tag;
       -- from tft.video join tft.tags on unnest(tft.video.tags) = tft.tags.tag;
       from (select id as vid, unnest(tags) as vtag from tft.video) join 
            (select id as tid, tag)
       on  vtag = tag
    end;
$$
