# Parser and Cubes-based OLAP visualizer for family budget in XLS format

## Quick introduction

This set of scripts allows for extraction of raw income and spending
data from an XLS-file ("family budget"), parsing them and combining
into a dataset (SQLite), that is compatible with [Cubes][1] framework and
[CubesViewer][2] visualization.

### To create a database:

Run `alembic upgrade head`

### To append to a database:

Put the XLS-file into the `source-data` folder of this project and run the
program as

```python script.py [--fromdate YYYY-MM-DD] --filename=source-data/<filename.xls>```

If `fromdate` is specified, parser will overwrite all data that might
be stored in a database, that are later than the date specified,
otherwise it will find the latest date in the database and start off
with it

### To visualize the data:

Run

```slicer serve slicer.ini```

([Cubes][1] has to be installed!). In order to view the tabs, charts,
and all the awesome stuff, open `views.html` from [CubesViewer][2]
download.

Here's an example of some of the beauty it provides:

![Screenshot](/images/fambudget1.png "Example of visualization")

[1]: https://pythonhosted.org/cubes/index.html
[2]: http://www.cubesviewer.com/