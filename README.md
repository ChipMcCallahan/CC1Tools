# CC1Tools
Assorted tools for working with and displaying [Chip's Challenge](https://wiki.bitbusters.club/Main_Page) levelsets and levels in [DAT file format](http://www.seasip.info/ccfile.html). Some of the important components are described below.

### Protocol Buffers and Utilities
[Levelset](https://github.com/ChipMcCallahan/CC1Tools/blob/4516095d514873ec3cccff0c1cd7564c5a163c8c/src/cc1_levelset.proto#L10) class: A protocol buffer representing a CC1 Levelset. Consists of a name, an array of levels, and an experimental array of Story elements. It exists because it is much easier to work with than DAT files, and can be easily written back to DAT format using the CC1LevelsetWriter.

[Level](https://github.com/ChipMcCallahan/CC1Tools/blob/4516095d514873ec3cccff0c1cd7564c5a163c8c/src/cc1_levelset.proto#L28) class: A protocol buffer representing a CC1 Level, including the level map, the trap and clone controls, the movement list, and all the usual metadata from the DAT file.

[CC1TileCode](https://github.com/ChipMcCallahan/CC1Tools/blob/4516095d514873ec3cccff0c1cd7564c5a163c8c/src/cc1_levelset.proto#L51) enum: Enumeration of all of the object codes used to represent elements in DAT files.

[CC1Levels.py](https://github.com/ChipMcCallahan/CC1Tools/blob/main/src/CC1Levels.py) functions: Highly useful utility functions for adding and removing elements to a Level object. These functions automatically keep the clone/trap controls and movement lists updated as elements are placed or deleted. They also keep the top/bottom layers up to date to ensure the level validity is maintained (e.g. if a mob is placed on a tile with terrain, the terrain will be moved to the bottom layer. If the mob is then removed, the terrain is returned to the top layer.)

[CC1TileCodes.py](https://github.com/ChipMcCallahan/CC1Tools/blob/main/src/CC1TileCodes.py) functions and prebuilt element sets: Utilities for working with CC1TileCode enums. Provides useful groupings of similar elements, for example the set CC1TileCodes.TANKS contains the N, E, S, and W version of the blue tank. Also provides functions to rotate or reverse tile codes (e.g. `CC1TileCodes.rotate_right(CC1TileCode.TANK_N)` would yield `CC1TileCode.TANK_E`).

(See examples of using the protobufs and utilities in the [CC1LevelsetProto Jupyter notebook](https://github.com/ChipMcCallahan/CC1Tools/blob/main/colab/cc1_levelset_proto.ipynb) or try it out now with full functionality [in your browser](https://colab.research.google.com/github/ChipMcCallahan/CC1Tools/blob/main/colab/cc1_levelset_proto.ipynb)).

### Levelset Imports, Reads, and Writes
[CC1LevelsetImporter](https://github.com/ChipMcCallahan/CC1Tools/blob/main/src/CC1LevelsetImporter.py) class: Lists available custom CC1 levelsets from the [Bit Busters Club](https://bitbusters.club/) fan website, and imports them by name. (e.g. `importer.get_set("CCLP1.dat")` would retrieve the raw DAT file).

[DATReader](https://github.com/ChipMcCallahan/CC1Tools/blob/4516095d514873ec3cccff0c1cd7564c5a163c8c/src/CC1LevelsetReader.py#L19) class: Converts a raw DAT file into a `Levelset` proto.

[CC1LevelsetReader](https://github.com/ChipMcCallahan/CC1Tools/blob/4516095d514873ec3cccff0c1cd7564c5a163c8c/src/CC1LevelsetReader.py#L124) class: Imports and converts custom sets to `Levelset` proto format. Combination of the `CC1LevelsetImporter` and `DATReader` functionality.

[CC1LevelsetWriter](https://github.com/ChipMcCallahan/CC1Tools/blob/4516095d514873ec3cccff0c1cd7564c5a163c8c/src/CC1LevelsetWriter.py#L31) class: Writes a `Levelset` proto to DAT format.

(See examples of Levelset Imports, Reads, and Writes in the [CC1LevelsetIO Jupyter notebook](https://github.com/ChipMcCallahan/CC1Tools/blob/main/colab/cc1_levelset_io.ipynb) or try it out now with full functionality [in your browser](https://colab.research.google.com/github/ChipMcCallahan/CC1Tools/blob/main/colab/cc1_levelset_io.ipynb)).

### Other Utilities
[CC1LevelImager](https://github.com/ChipMcCallahan/CC1Tools/blob/main/src/CC1LevelImager.py) class: Provides very basic functionality for visualizing levels. It uses CC2 artwork and is incomplete (e.g. it cannot show trap/clone controls, movement order, or buried tiles). (See examples in the [CC1LevelImager Jupyter notebook](https://github.com/ChipMcCallahan/CC1Tools/blob/main/colab/cc1_level_imager.ipynb) or try it out now with full functionality [in your browser](https://colab.research.google.com/github/ChipMcCallahan/CC1Tools/blob/main/colab/cc1_level_imager.ipynb)).

[CC1LevelsetTransformer](https://github.com/ChipMcCallahan/CC1Tools/blob/main/src/CC1LevelsetTransformer.py) class: Allows applying simple rules to transform levels and levelsets element-wise (e.g. removing all non-wall tiles to create a "Walls Of" set, or replacing all monsters with a single monster type to create a "Blobs Of" set). (See examples in the [CC1LevelsetTransformer Jupyter notebook](https://github.com/ChipMcCallahan/CC1Tools/blob/main/colab/cc1_levelset_transformer.ipynb) or try it out now with full functionality [in your browser](https://colab.research.google.com/github/ChipMcCallahan/CC1Tools/blob/main/colab/cc1_levelset_transformer.ipynb)).

[CC1RandomLevelsetGenerator](https://github.com/ChipMcCallahan/CC1Tools/blob/main/src/CC1RandomLevelsetGenerator.py) class: Facilitates creating a levelset by randomly selecting levels from other levelsets, with various simple options available to filter the pool of eligible levels. This could be useful for setting up a speedrun competition, for example. (See examples in the [CC1RandomLevelsetGenerator Jupyter notebook](https://github.com/ChipMcCallahan/CC1Tools/blob/main/colab/cc1_random_levelset_generator.ipynb) or try it out now with full functionality [in your browser](https://colab.research.google.com/github/ChipMcCallahan/CC1Tools/blob/main/colab/CC1RandomLevelsetGenerator.ipynb)).




