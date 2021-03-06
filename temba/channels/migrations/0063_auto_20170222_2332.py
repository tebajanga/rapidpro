# Generated by Django 1.10.5 on 2017-02-22 23:32

from django.db import migrations

SQL = """
DROP TRIGGER IF EXISTS temba_channellog_update_channelcount ON channels_channellog;

CREATE TRIGGER temba_channellog_update_channelcount
   AFTER INSERT OR DELETE OR UPDATE OF is_error, channel_id
   ON channels_channellog
   FOR EACH ROW
   EXECUTE PROCEDURE temba_update_channellog_count();

----------------------------------------------------------------------
-- Manages keeping track of the # of messages in our channel log
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_update_channellog_count() RETURNS TRIGGER AS $$
BEGIN
  -- ChannelLog being added
  IF TG_OP = 'INSERT' THEN
    -- Error, increment our error count
    IF NEW.is_error THEN
      PERFORM temba_insert_channelcount(NEW.channel_id, 'LE', NULL::date, 1);
    -- Success, increment that count instead
    ELSE
      PERFORM temba_insert_channelcount(NEW.channel_id, 'LS', NULL::date, 1);
    END IF;

  -- Updating is_error is forbidden
  ELSIF TG_OP = 'UPDATE' THEN
    RAISE EXCEPTION 'Cannot update is_error or channel_id on ChannelLog events';

  -- Deleting, decrement our count
  ELSIF TG_OP = 'DELETE' THEN
    -- Error, decrement our error count
    IF OLD.is_error THEN
      PERFORM temba_insert_channelcount(OLD.channel_id, 'LE', NULL::date, -1);
    -- Success, decrement that count instead
    ELSE
      PERFORM temba_insert_channelcount(OLD.channel_id, 'LS', NULL::date, -1);
    END IF;

  -- Table being cleared, reset all counts
  ELSIF TG_OP = 'TRUNCATE' THEN
    DELETE FROM channels_channel WHERE count_type IN ('LE', 'LS');
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;
"""


class Migration(migrations.Migration):

    dependencies = [("channels", "0062_auto_20170208_1450")]

    operations = [migrations.RunSQL(SQL)]
