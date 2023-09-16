import datapane as dp 

top_10_tracks_query = '''
SELECT 
    t.name trackname,
    a.title album_title,
    ar.name artist,
    COUNT(*) as total_purchases,
    SUM(il.unit_price) total_cost
FROM track t 
JOIN album a on a.album_id = t.album_id
JOIN artist ar on ar.artist_id = a.artist_id
JOIN invoice_line il on il.track_id = t.track_id
GROUP BY 1
ORDER BY total_purchases desc
LIMIT 10
'''

top_10_df = run_query(top_10_tracks)

dp.Report(
    dp.DataTable(top_10_df)
).publish(name="Music Sales")