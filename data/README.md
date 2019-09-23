# Taxon Data

Download taxdump.zip/.tar.gz from ftp://ftp.ncbi.nih.gov/pub/taxonomy/ and extract it to this folder. Only nodes.dmp and
names.dmp are currently used.

If sequencer.default_settings.LOAD_TAXON_DATA is true, this data will be loaded into taxonomy tables in the app.
(Note that, as of this writing, these tables are unused, so this is an entirely optional step.)

Refer to readme.txt (supplied in the zip) for more information about these files.
