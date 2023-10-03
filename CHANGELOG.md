# CHANGELOG



## v0.6.3 (2023-10-03)

### Fix

* fix: fix issue of merged values when parsing report file ([`4e249d6`](https://github.com/oopnet/oopnet/commit/4e249d650de0af038b7a731b4737294de1de29da))

### Unknown

* Merge pull request #48 from oopnet/fix/report_parsing_decimals

Fix report parsing decimals and deprecated pandas methods ([`266dd0c`](https://github.com/oopnet/oopnet/commit/266dd0c266c479f4ff7c0dcf105f9f6b4c545631))

* replace deprecated pandas methods iterrows and applymap ([`5c4dcb1`](https://github.com/oopnet/oopnet/commit/5c4dcb107362bb1f9043080074ae1590b05ab652))


## v0.6.2 (2022-10-22)

### Fix

* fix: fixed minor bug in ReportFileReader ([`43a8fca`](https://github.com/oopnet/oopnet/commit/43a8fcafb3024d25604343d26c79a36e869092bc))


## v0.6.1 (2022-10-15)

### Fix

* fix: fixed a bug where Valves in controls resulted in an invalid EPANET model

EPANET does not accept FCV/PCV/PRV/... in the IF line in controls but requires VALVE instead. The THEN line accepts VALVE however. Added a corresponding rule to Rules_network and. ([`1c20957`](https://github.com/oopnet/oopnet/commit/1c20957cb8a665997f7379a9af561e6ea46222e7))

### Unknown

* Merge remote-tracking branch &#39;origin/main&#39; ([`a82d833`](https://github.com/oopnet/oopnet/commit/a82d833a16b2c9644110fff22d0a621f2d218f3b))

* [skip ci] docs: fixed figure in plotting userguide ([`1d6a008`](https://github.com/oopnet/oopnet/commit/1d6a008c9454c8a499479d0e55b3551daa62fcd3))


## v0.6.0 (2022-10-07)

### Documentation

* docs: recreated plots with new, stacked color bars and added example for ax argument ([`60bc691`](https://github.com/oopnet/oopnet/commit/60bc69179ab0cdee4614464a0192a1d1f288cab7))

* docs: added missing argument documentation to pyplot NetworkPlotter.animate() ([`6b29827`](https://github.com/oopnet/oopnet/commit/6b298270d8b1fe2850e1ab5b99f00b37a3d6c5d9))

### Feature

* feat: matplotlib colorbars are now stacked if both `nodes` and `links` arguments are passed ([`6523fd8`](https://github.com/oopnet/oopnet/commit/6523fd806ea849a1382f8829529069fcbfccf676))

### Unknown

* Merge remote-tracking branch &#39;origin/main&#39; ([`b213f72`](https://github.com/oopnet/oopnet/commit/b213f725ecf940d7a21bbb1226b170c5e0abf41a))

* [skip ci] docs: added missing figure in plotting userguide ([`d5fe95a`](https://github.com/oopnet/oopnet/commit/d5fe95a2b612b0f41f2008fcc516c867d18329c8))

* Merge remote-tracking branch &#39;origin/main&#39; ([`bf520f5`](https://github.com/oopnet/oopnet/commit/bf520f5137a029f477e0448ebbfcf79d92884a37))

* [skip ci] docs: renamed OOPNET to Object-Oriented Pipe Network Analyzer ([`7a5682d`](https://github.com/oopnet/oopnet/commit/7a5682d7f3bc1e987df77cc045ab6d0c64274ac2))

* Merge remote-tracking branch &#39;origin/main&#39; into plt_colorbars ([`b489351`](https://github.com/oopnet/oopnet/commit/b4893511fc0d7ddd7b2106384571e43acbe3d558))


## v0.5.3 (2022-10-05)

### Fix

* fix: bugfix in ReportFileReader

fixed another bug, where concatenated results are not parsed correctly ([`2dad842`](https://github.com/oopnet/oopnet/commit/2dad8422c260974d81b9da04a60e21475ae3c6fd))


## v0.5.2 (2022-09-26)

### Fix

* fix: ReportFileReader bugfix

fixed a bug where concatenated large values are not split correctly if they appear in the first line of a result block ([`127f1ce`](https://github.com/oopnet/oopnet/commit/127f1cec0a47a7ab1b6932a5701085be961f0a86))


## v0.5.1 (2022-09-22)

### Ci

* ci: deactivated black formatting ([`a69d815`](https://github.com/oopnet/oopnet/commit/a69d815c63d11a5c8daaefa310318da209057e56))

### Fix

* fix: fixed demand category bug

- fixed demand category reading and writing
- added test for demand category reading and writing
- added demand categories to Junction J-02 in Poulakis_enhanced_PDA.inp and updated results file ([`e150b00`](https://github.com/oopnet/oopnet/commit/e150b00c63e3c1e159a089731a2b77566befa380))

### Test

* test: merged animation plotting tests into one to speed up tests ([`8307053`](https://github.com/oopnet/oopnet/commit/83070534e3843a20f058e93fc97926b408775d11))

### Unknown

* [ci skip] updated feature request template

added example code block ([`e30a98d`](https://github.com/oopnet/oopnet/commit/e30a98d5b3b12ec25fe0be36f9c775b94aec01ed))

* [ci skip] bug report template update

added example code block ([`49dc49b`](https://github.com/oopnet/oopnet/commit/49dc49bf1c82279301f66eb817176cb64c0e0c4b))

* started fixing colorbar positioning and sizing ([`1e7d7ba`](https://github.com/oopnet/oopnet/commit/1e7d7bab82e767c6090a5ce1946c3a5bec684c66))

* [ci skip] rtd bugfix ([`5493ae0`](https://github.com/oopnet/oopnet/commit/5493ae00c607c7bc36bffb120f1bf77ebab31e4f))

* [ci skip] rtd bugfix ([`8fa7909`](https://github.com/oopnet/oopnet/commit/8fa7909e6f331eb33655c3581820539c31602995))

* [ci skip] rtd bugfix ([`dbdf000`](https://github.com/oopnet/oopnet/commit/dbdf00078411e4bf85477e6191a62528306d991b))

* [ci skip] rtd bugfix ([`cdf9676`](https://github.com/oopnet/oopnet/commit/cdf96764dd2ea7a7adddb34cdcd7dba795381515))

* [ci skip] rtd bugfix ([`21497a9`](https://github.com/oopnet/oopnet/commit/21497a96c5379206351d652d68de58dd0d01ad1d))

* [ci skip] rtd bugfix ([`1d8c4d2`](https://github.com/oopnet/oopnet/commit/1d8c4d217a5a6af8eb56d2b2e294d8d8a4657da0))

* [ci skip] rtd bugfix ([`79ab631`](https://github.com/oopnet/oopnet/commit/79ab63198dc1c31b0d07bb0d9348556305e3cf40))

* [ci skip] rtd bugfix ([`b788ca0`](https://github.com/oopnet/oopnet/commit/b788ca0f314bf8d1b43fb21005052f8e2e5bb58d))

* [ci skip] added pre_install job to install EPANET in the rtd environment ([`6655b31`](https://github.com/oopnet/oopnet/commit/6655b31d7f01559d9ae4533aaff686a96254fdef))

* [ci skip] fix bokeh plot in docs

* docs: updated examples

* docs: created user guide from old examples

+ fixed minor errors related to docstrings and type hints for the documentation
+ added some missing example script tests
+ added a documentation status badge to README.md
+ started revising about.rst

* added missing extended_period_simulation.png

* added plotting figures, fixed bokeh plot visualization in sphinx docs

* fixed path to license file in README.md

* added startdatetime argument passing in simulation example

* some more doc updates, typo corrections, citations, ...

* created dedicated bokeh plot script for docs ([`13a2c15`](https://github.com/oopnet/oopnet/commit/13a2c15d7f10a17b3de101928c8d88ad6ee04c99))

* [ci skip] Documentation update from docs branch

* docs: updated examples

* docs: created user guide from old examples

  + fixed minor errors related to docstrings and type hints for the documentation
  + added some missing example script tests
  + added a documentation status badge to README.md
  + started revising about.rst

* added missing extended_period_simulation.png

* added plotting figures, fixed bokeh plot visualization in sphinx docs

* fixed path to license file in README.md

* added startdatetime argument passing in simulation example

* some more doc updates, typo corrections, citations, ... ([`d1127d8`](https://github.com/oopnet/oopnet/commit/d1127d8387b5e506f612b6e28cd2cb1c70aeb6e6))


## v0.5.0 (2022-09-18)

### Documentation

* docs: renamed LICENSE to LICENSE.md to use markdown ([`08a1e69`](https://github.com/oopnet/oopnet/commit/08a1e6958e4ff9444ba9d9f209893cd6630bc932))

### Feature

* feat: added a new NetworkPlotter class that enables static plots and animations

- replaced PlotSimulation, Plotnodes etc. with a single class for plotting
- implemented a new animation function to visualize extended period simulations
- added `animate` method to Network class
- added documentation and a new example run_and_animate.py base on L-Town
- added tests ([`3a3a028`](https://github.com/oopnet/oopnet/commit/3a3a02840443009cffb2d9d271402bb4c7123855))

* feat: added `center` method to Link components to calculate a Link&#39;s geometric center in 2D

center coordinates are derived from start and end nodes, as well as vertices
does not take component&#39;s length attribute into account
useful for plotting ([`d3f5dbf`](https://github.com/oopnet/oopnet/commit/d3f5dbff5f5e7f2e175206fa7a6b2d7fb020711f))

### Fix

* fix: switched SimulationReport property type hints to Union[pd.Series, pd.DataFrame] to take extended period simulations into account ([`2ffcccc`](https://github.com/oopnet/oopnet/commit/2ffcccc635849a9528fb76e46f7a64dacef4e99f))

### Refactor

* refactor: reformatted by black ([`1666128`](https://github.com/oopnet/oopnet/commit/1666128b59e04ce341f26f956dbe5a9a81cdec61))

### Test

* test: fixed simulation tests by adding sort_index call ([`f10671f`](https://github.com/oopnet/oopnet/commit/f10671f716147046ef8876f74d814f3fac8fe0b2))

* test: added test for Link center calculation ([`493cfe2`](https://github.com/oopnet/oopnet/commit/493cfe2cad0c98d39537000039f30255b690af5b))

### Unknown

* Merge pull request #41 from oopnet/animation_plotting

Animation plotting
Fixes #39 ([`7a5bb8a`](https://github.com/oopnet/oopnet/commit/7a5bb8aed272e260c2e09fb605cbabf8a856d327))

* added scyipy to requirements-dev.txt ([`ab1e02c`](https://github.com/oopnet/oopnet/commit/ab1e02c7ebc69c057e3cc50e3d16b3502760f39d))


## v0.4.1 (2022-09-02)

### Fix

* fix: added sort_index() call to pandas results ([`53545ca`](https://github.com/oopnet/oopnet/commit/53545ca621afce3b6f36663100e9228e306c788f))

### Test

* test: fixed simulator test ([`33dce6c`](https://github.com/oopnet/oopnet/commit/33dce6cb762be27b4dc76c879e3275010e2f05ba))


## v0.4.0 (2022-09-01)

### Documentation

* docs: updated information in setup.cfg for PyPI ([`e6f23b5`](https://github.com/oopnet/oopnet/commit/e6f23b52a28b0b10475179221a91c550d6e9064b))

* docs: added badges to README.md ([`d131b8a`](https://github.com/oopnet/oopnet/commit/d131b8adbac0e361ca12809c2ee856cf7b834bee))

### Feature

* feat: added vertex plotting to Bokeh plot ([`4ebe022`](https://github.com/oopnet/oopnet/commit/4ebe02261672f06268f9d666f869e62ffcb5b73c))

### Fix

* fix: switched condition attribute default of Rules from None to an empty list ([`aad8f00`](https://github.com/oopnet/oopnet/commit/aad8f00bb9095cee65967e5f6ba52a03c0e15273))

* fix: fixed reading time options in hh:mm:ss format ([`fa2abef`](https://github.com/oopnet/oopnet/commit/fa2abef883af201a91924b4396a7221ca2389caa))

### Unknown

* [ci skip] ci: switched to dedicated user (OOPNET-bot) for CI pipelines ([`c58173b`](https://github.com/oopnet/oopnet/commit/c58173b742671f52b93faf34d50b77740a84dd30))


## v0.3.2 (2022-08-26)

### Ci

* ci: added check to skip pipeline execution if a commit was triggered by OOPNET-bot ([`b9a2f21`](https://github.com/oopnet/oopnet/commit/b9a2f21ac00a6f3e69d4c4b390bb23634b61edfe))

### Documentation

* docs: corrected Network attribute documentation ([`3a71dd9`](https://github.com/oopnet/oopnet/commit/3a71dd9c26ee3aae277b80cc524dc313d662dd8c))

### Fix

* fix: fixed concatenated large number parsing error in report file reader

fixes #34 ([`1685835`](https://github.com/oopnet/oopnet/commit/1685835e1d16bf7eaa605e829486ddde07e4d5de))

* fix: moved parts of report module to simulator module for better consistency ([`41ca790`](https://github.com/oopnet/oopnet/commit/41ca7907043fd718c40fc0c5bf060bdba37be7e9))

### Unknown

* ci bugfix ([`16ec2d7`](https://github.com/oopnet/oopnet/commit/16ec2d77a18d0bb8134973449a5c90cc7f5dc337))

* ci bugfix ([`fc7aa0a`](https://github.com/oopnet/oopnet/commit/fc7aa0ae6d600f76e28e7092826831fe0ac44586))

* ci bugfix ([`fe85d50`](https://github.com/oopnet/oopnet/commit/fe85d507afac61cd4c4962034ad617d156e8006e))

* ci bugfix ([`3bec184`](https://github.com/oopnet/oopnet/commit/3bec184484613dea6e9cc93490db6db94c888010))

* Merge pull request #35 from oopnet/docs

Large number parsing fix ([`9111738`](https://github.com/oopnet/oopnet/commit/91117381185c7c42cf6e2f876f2097b2ae2dbbbf))

* [ci-skip] added ReadTheDocs configuration yml ([`6df531c`](https://github.com/oopnet/oopnet/commit/6df531cde00598b5e84fe30c6bfdfe50ef6cd10b))

* [ci-skip] added pull request template ([`d50c962`](https://github.com/oopnet/oopnet/commit/d50c96219c2c459b969d2675678c9c2452f952e4))

* [ci-skip] added README.md prototype ([`f0602c2`](https://github.com/oopnet/oopnet/commit/f0602c2e3a626045f67b9d8f2db3817d19389ffc))

* [ci-skip] added checks to bug report template ([`0890afd`](https://github.com/oopnet/oopnet/commit/0890afdcb902188a6694937063d6390461a34bbe))

* [ci-skip] Update issue templates ([`fda2548`](https://github.com/oopnet/oopnet/commit/fda254804a113fe768b9c70dc7ac357a69711776))

* Automated changes ([`a4426f0`](https://github.com/oopnet/oopnet/commit/a4426f0788015f7175302c56926aee136c4842e1))

* [ci-skip] docs: added doc building requirements to requirements-dev.txt ([`3dfa65f`](https://github.com/oopnet/oopnet/commit/3dfa65f0dfe9b0f62b5d2d1bbd4c04811966913e))

* [ci-skip] doc refactoring (#29)

* [ci skip] added CONTRIBUTING.md and CODE_OF_CONDUCT.md

* [ci skip] added link to code of conduct to CONTRIBUTING.md

* [ci skip] updated CONTRIBUTING.md

* [ci skip] updated email addresses

* [ci skip] docs: documentation refactoring

- switched from readthedocs to mkdocs-like documentation
- restructured documentation layout
- restructured documentation files
- moved old into new docs
- corrected mistakes in a few examples
- switched LICENSE to LICENSE.md to include it in the docs
- removed old doc directory ([`91f4ade`](https://github.com/oopnet/oopnet/commit/91f4ade986010ad6eeb4f0748fad6e87dc175f09))

* [ci skip] updated email address ([`e2beb60`](https://github.com/oopnet/oopnet/commit/e2beb607d33281025fb921803ae329464a9602b3))

* [ci skip] adapted code of conduct ([`4bdcd41`](https://github.com/oopnet/oopnet/commit/4bdcd419a29ee58cf8c5de451da6f972b32374d8))

* Dev (#27)

* [ci skip] added CONTRIBUTING.md and CODE_OF_CONDUCT.md

* [ci skip] added link to code of conduct to CONTRIBUTING.md

* [ci skip] updated CONTRIBUTING.md ([`9881bd2`](https://github.com/oopnet/oopnet/commit/9881bd29b10d1e13ce584f1868981d4162935dcb))

* [ci skip] added CONTRIBUTING.md and CODE_OF_CONDUCT.md ([`763e086`](https://github.com/oopnet/oopnet/commit/763e086dbcfb9f4dd89a1b89ad40a5ace058d162))

* [ci skip] Update issue templates ([`72dc04d`](https://github.com/oopnet/oopnet/commit/72dc04de16a41062128b53e43f4581263ab9281d))


## v0.3.1 (2022-04-14)

### Fix

* fix: fixed a bug where networkx get_edge_data returning a dict instead of a list breaks nxedge2onlink_id ([`8377d16`](https://github.com/oopnet/oopnet/commit/8377d16a09b0e9a23820db2af7820fa627242a1f))


## v0.3.0 (2022-02-28)

### Ci

* ci: fixed pipeline ([`635fe88`](https://github.com/oopnet/oopnet/commit/635fe88511e4c6fccdeab9ce9b18533096eecc2a))

### Feature

* feat: added get_by_id method to SuperComponentRegistry for NetworkComponent lookup

get_by_id is a utility function for iterating over all ComponentRegistries stored in a SuperComponentRegistry. It is implemented in get_nodes(network) and get_links(network). ([`d89c8cc`](https://github.com/oopnet/oopnet/commit/d89c8cc88bb7ab979ec73a0a7b8e3d18c1c40d49))

### Fix

* fix: renamed Tank attribute diam to diameter

+ adapted tests, writer, reader ... ([`0f6801d`](https://github.com/oopnet/oopnet/commit/0f6801d03d755ba2e5ef85773309a2e0af5fed03))

* fix: fixed some type hints

Added lists to the appropriate class attributes ([`91b3a6e`](https://github.com/oopnet/oopnet/commit/91b3a6eda9fae12a07e36adcbb91b527cab3c9ed))

### Unknown

* Automated changes ([`9283b91`](https://github.com/oopnet/oopnet/commit/9283b91964bd5bda6f8e30218010541cfd527be4))


## v0.2.3 (2022-02-22)

### Fix

* fix: fixed ComponentRegistry pickling

quick fix to prevent pickling error of ComponentRegistries (object of type ComponentRegistry has no attribute super_registry) ([`fbe2900`](https://github.com/oopnet/oopnet/commit/fbe290064dd353fdca969630cbfa6acac525c106))

### Test

* test: added tests for pickling Networks and SimulationReports ([`dfbc9f2`](https://github.com/oopnet/oopnet/commit/dfbc9f27aa38ca83b123c1578fd1505cddb30d8e))

* test: added tests for adding different component types with same ID

test for e.g. adding a Junction with ID &#34;1&#34; to a Network that already contains a Tank with the ID &#34;1&#34; ([`3fd5818`](https://github.com/oopnet/oopnet/commit/3fd58185b369a21b6243e194cb734181eef1ba93))


## v0.2.2 (2022-02-22)

### Ci

* ci: switched to OOPNET_SECRET for pushing changes ([`851a087`](https://github.com/oopnet/oopnet/commit/851a08755b8ba0a22029849f957cab452791f7b0))

### Fix

* fix: disabled testing the mc stereo scoop example

SCOOP isn&#39;t working with Python 3.10 as described in [this issue](https://github.com/soravux/scoop/issues/94) ([`003f249`](https://github.com/oopnet/oopnet/commit/003f249099a40d6b5c647571c0b8ef48f3be8fca))

* fix: fixed CI pipeline

replaced Python version 3.10 with &#34;3.10&#34; to prevent trimming the version to 3.1 ([`50f2650`](https://github.com/oopnet/oopnet/commit/50f2650ea56249cb58d247210d41443c2d194283))

* fix: fixed CI pipeline

CI pipeline now takes all commits since last release instead of latest only
added tests for Python 3.10
minor changes to semantic release secrets ([`b79726c`](https://github.com/oopnet/oopnet/commit/b79726cbda8e37cd1cd9c675146f3b43cf67b15a))

* fix: fixed ComponentRegistry initialization

removed dataclass decorator since it could lead to issues ([`1cd7d64`](https://github.com/oopnet/oopnet/commit/1cd7d64184856de6b2633a1ceda4dbc2038e3ebe))

### Refactor

* refactor: minor changes to component registries and network annotations ([`cdb7471`](https://github.com/oopnet/oopnet/commit/cdb74711c776e82f9f13cd1793a2b1fa7a9a79c5))

### Test

* test: added some new tests (patterns, curve, deepcopy)

+ added model for curve and pattern testing and added some tests
+ wrote some deepcopy tests ([`1240cba`](https://github.com/oopnet/oopnet/commit/1240cba5e0a652e13bfb07f0715dea8e41cc8ac9))

### Unknown

* Automated changes ([`d00fb36`](https://github.com/oopnet/oopnet/commit/d00fb360d94fb6ed5d1b5a3a9dee922798fc9901))


## v0.2.1 (2022-02-17)

### Fix

* fix: fixed writing Tank volumecurves ([`960a232`](https://github.com/oopnet/oopnet/commit/960a23287042eb8f20012748c4fbbca38f959a7e))


## v0.2.0 (2022-02-14)

### Feature

* feat: added linkwidth argument to Network.plot

Linkwidth takes a pandas Series with values describing the width of specific Pipes (!).
Added tests for some other plotting arguments as well. ([`f749a48`](https://github.com/oopnet/oopnet/commit/f749a4803e5583bea126791ed2c54e28a1059b6f))

### Fix

* fix: fixed pandas Series for links with missing values

Missing values from a link pandas Series don&#39;t lead to an error anymore when looking up the color of the missing Link. Black will be used instead. ([`cc681f4`](https://github.com/oopnet/oopnet/commit/cc681f440ee9393691ab41ffcdbdebbdcc61907d))

* fix: added ComponentExistsError to __init__.py and renamed to IdenticalIDError ([`cde55a0`](https://github.com/oopnet/oopnet/commit/cde55a01e051b5cb62190dcb5fc6c33629d10290))

* fix: fixed Pipe split function

Fixed pipe length calculation, added validation for split_ratio argument and added logging (DEBUG level).
Added tests for invalid split_ratio arguments and enhanced existing tests. ([`7e3b53a`](https://github.com/oopnet/oopnet/commit/7e3b53a4b92a74b5cae46bc33a9cd0d11f143bb6))

### Refactor

* refactor: refactored benchmark.py to incorporate new Network API ([`4f5d9bd`](https://github.com/oopnet/oopnet/commit/4f5d9bde11134cf6a50b3bec1cd0439a3ae18544))


## v0.1.6 (2022-02-07)

### Ci

* ci: added dedicated pull request workflow

Added dedicated PR workflow to prevent building OOPNET when adding a PR ([`dc9549a`](https://github.com/oopnet/oopnet/commit/dc9549a1adb3a939ab61cc3d21e1586be926a3bf))

* ci: added dedicated pull request workflow

Added dedicated PR workflow to prevent building OOPNET when adding a PR ([`2ae988c`](https://github.com/oopnet/oopnet/commit/2ae988c02b893fd415e7c3d6b09997c4bdba9bb3))

### Fix

* fix: minor changes to setup.cfg to trigger release ([`18b3df2`](https://github.com/oopnet/oopnet/commit/18b3df2a166bd0ae575b128d0f5753755428acc1))

* fix: minor changes to setup.cfg to trigger release ([`4456b9e`](https://github.com/oopnet/oopnet/commit/4456b9e2b63d702f19f8bb44aadc3c0d1867f12f))

* fix: fixed Network creation from strings

added tests for contentreading ([`a5afc67`](https://github.com/oopnet/oopnet/commit/a5afc675b8901c3b3fe950982610162f00af026c))

* fix: Headloss of Pumps is now correctly returned ([`c53f22c`](https://github.com/oopnet/oopnet/commit/c53f22c122ebce31d473771eab92f4dd1f678913))

### Refactor

* refactor: removed vertices from Network ([`39c5fe1`](https://github.com/oopnet/oopnet/commit/39c5fe1550e74ef2992d53db0b22108b09c06266))

* refactor: set explicit dtypes for pandas Series in property_getters.py

silencing pandas warning ([`f19fb16`](https://github.com/oopnet/oopnet/commit/f19fb16113256810eba3e96c0d1f57437a100611))

### Test

* test: added missing Poulakis_enhanced_PDA.xlsx for SimulatorTests ([`be5774a`](https://github.com/oopnet/oopnet/commit/be5774a3fc902a2c93603a4bbfe2a4da3577a7c9))

* test: added missing Poulakis_enhanced_PDA.xlsx for SimulatorTests ([`50714a7`](https://github.com/oopnet/oopnet/commit/50714a791c6baf89f0d19bd18168418168b9de76))

* test: added SimulatorTest for PoulakisEnhancedModel ([`9c084a8`](https://github.com/oopnet/oopnet/commit/9c084a8d93460b309fecec46ba94ceaf93935538))

### Unknown

* Merge pull request #22 from oopnet/dev

Dev ([`ac64888`](https://github.com/oopnet/oopnet/commit/ac64888bf5cb3b7673086272dab4b2153a0a9c16))

* Automated changes ([`bb6aecb`](https://github.com/oopnet/oopnet/commit/bb6aecb3ad4d92e6425766eace0ffa2ee6fa389b))

* Automated changes ([`9f0dca0`](https://github.com/oopnet/oopnet/commit/9f0dca018b0025afa990e1ed47b2728acbf49c3f))

* Merge pull request #21 from oopnet/dev

Dev ([`0799437`](https://github.com/oopnet/oopnet/commit/0799437ab2b2792a23eaa016aadc2c92efc0dc18))


## v0.1.5 (2022-02-07)

### Fix

* fix: fix CI ([`98053e7`](https://github.com/oopnet/oopnet/commit/98053e7775ce0d87a239ea991e4905070f8a463f))

* fix: fix CI ([`460c190`](https://github.com/oopnet/oopnet/commit/460c190421c1ebb44e953d65fa3fcc322b7af565))

* fix: fix CI ([`3f655eb`](https://github.com/oopnet/oopnet/commit/3f655eb0a92b15a967aa4272bd5e6037a9cd3718))

* fix: fix CI ([`4d38518`](https://github.com/oopnet/oopnet/commit/4d385188b43f84044f27a31914ffae31d6a943d9))

* fix: another setup.cfg fix + slight CI changes ([`8eb5f38`](https://github.com/oopnet/oopnet/commit/8eb5f3842c9e85051684c2ac6404940869ae32c5))


## v0.1.4 (2022-02-06)

### Fix

* fix: another setup.cfg fix ([`40e8eb8`](https://github.com/oopnet/oopnet/commit/40e8eb81d6a87839029de4566861539cd6d067c6))


## v0.1.3 (2022-02-06)

### Fix

* fix: moved requirements from requirements.txt to setup.cfg to enable autoinstall of missing packages ([`eb119cd`](https://github.com/oopnet/oopnet/commit/eb119cd954d35f4ad49b1625651d3a2167e5c7a7))


## v0.1.2 (2022-02-06)

### Fix

* fix: fixed setup.cfg package_data ([`c3f7122`](https://github.com/oopnet/oopnet/commit/c3f71223641b51a31b4e6e9282436480190a598b))


## v0.1.1 (2022-02-06)

### Fix

* fix: fixed setup.cfg license ([`4accf2d`](https://github.com/oopnet/oopnet/commit/4accf2d1038e4755bb5ec64b97c082f23376f2eb))


## v0.1.0 (2022-02-06)

### Documentation

* docs: some fixes in various docstrings ([`c8a02df`](https://github.com/oopnet/oopnet/commit/c8a02df63cb53865fee6525ea7e5932c9b65e55d))

### Feature

* feat: nonsense to create new release ([`617dee9`](https://github.com/oopnet/oopnet/commit/617dee993de458a42b374bc61a3eee834f699beb))

* feat: added SimulatorTest for C-Town model

- Friction Factors and Status are not checked currently
- only using feat to trigger a new release for testing purposes ([`9c410d9`](https://github.com/oopnet/oopnet/commit/9c410d926c7ef85b2b63fdf04d705ba5df2f9c7e))

### Refactor

* refactor: switched Valve settings to individual attributes like maximum pressure

- adapted reader, writer and tests ([`d9853b2`](https://github.com/oopnet/oopnet/commit/d9853b22f845279cb07d50f30fd6d53587a188ec))

### Test

* test: fixed data reading for SimulatorTests ([`c44d8b7`](https://github.com/oopnet/oopnet/commit/c44d8b7fab80f1fc5d8accb5f6c701f9f1af20fb))

* test: fixed data reading for SimulatorTests ([`9d1dae7`](https://github.com/oopnet/oopnet/commit/9d1dae7a06bd2e4b5d8c99c5c8edf549cb4f97a8))

* test: fixed exception tests ([`bd60b37`](https://github.com/oopnet/oopnet/commit/bd60b3737b97591d584ef85be1175256beb1e494))

* test: fixed exception tests ([`7df91e7`](https://github.com/oopnet/oopnet/commit/7df91e781685c31568dce8f62a7f3520bec9bdbf))

### Unknown

* fixed data reading for SimulatorTests ([`114c945`](https://github.com/oopnet/oopnet/commit/114c945a4194a284db63a229a5955ac51efb7cac))

* Automated changes ([`63996ed`](https://github.com/oopnet/oopnet/commit/63996eda2a4e53f7a22c607f6105ae302b78b4ab))

* Update setup.cfg ([`7d96993`](https://github.com/oopnet/oopnet/commit/7d96993a865814a11ae7995b426c6c791d115b64))

* added output=True for model simulation tests for better debugging ([`5bbca1d`](https://github.com/oopnet/oopnet/commit/5bbca1df8b122d380ab7b66ae889dfded8fae1c1))

* Update build.yml ([`65708c5`](https://github.com/oopnet/oopnet/commit/65708c5ed772cb608174e26aade40aabdc3bde2f))

* Update build.yml ([`ead3dad`](https://github.com/oopnet/oopnet/commit/ead3dade1276ab9f09557f853aff2857bed8711c))

* added requirements-dev.txt ([`b28d2d1`](https://github.com/oopnet/oopnet/commit/b28d2d16157a07817ff5da1f27de1c18694f932e))

* Update build.yml ([`1aa7441`](https://github.com/oopnet/oopnet/commit/1aa744133d6b9c802a5276d15da846f060ff348b))

* Update build.yml ([`2ce70e3`](https://github.com/oopnet/oopnet/commit/2ce70e3608d54a648d9dfb20e79cacac62bfa030))

* Update and rename python-app.yml to build.yml ([`1febe93`](https://github.com/oopnet/oopnet/commit/1febe93e14d093c9f184e1f0092245a273073616))

* Automated changes ([`c7e5f5e`](https://github.com/oopnet/oopnet/commit/c7e5f5e64a9e77d7ab26c296d7a5f9ab5ec0b3c9))

* refactor

- changed setup settings ([`07741d5`](https://github.com/oopnet/oopnet/commit/07741d59b48bed7593e7348722a54b70202622c8))

* refactor

- changed setup settings ([`9117ddb`](https://github.com/oopnet/oopnet/commit/9117ddba0edcb31e7dbed595a518dcb812d711da))

* refactor

- changed setup settings ([`3a5a197`](https://github.com/oopnet/oopnet/commit/3a5a197f7c9c919a3ce986ed01a517074a1697ee))

* refactor

- changed setup settings ([`2c3d732`](https://github.com/oopnet/oopnet/commit/2c3d732dac9e99bd541f5d183f544782fef451f1))

* Automated changes ([`7b748a5`](https://github.com/oopnet/oopnet/commit/7b748a59a5a83e096c9f0c23198b5a4e1a352fd9))

* refactor

- changed setup settings ([`4cdf32b`](https://github.com/oopnet/oopnet/commit/4cdf32bce30484f0a771121f95c38f77a13d09ac))

* refactor

- changed setup settings ([`4d165f5`](https://github.com/oopnet/oopnet/commit/4d165f5455f707b1cb6625c29b48176c6fb299a1))

* refactor

- added sematic_release section to setup.cfg
- added some classifiers to setup.cfg ([`9511323`](https://github.com/oopnet/oopnet/commit/9511323ca9f9ca9034e65404b26dacbe36e52c70))

* Automated changes ([`9dbd67f`](https://github.com/oopnet/oopnet/commit/9dbd67fc10e479ec869985dad25c95a5ec455564))

* refactor

- moved build settings to setup.cfg ([`f9f5bf6`](https://github.com/oopnet/oopnet/commit/f9f5bf6936d52c21052a0f88329e49cdb720c0aa))

* Update python-app.yml ([`ad0a46a`](https://github.com/oopnet/oopnet/commit/ad0a46a8c0c9126ff83282c8f870181f91b207bb))

* refactor

- moved __version__ to setup.py ([`7370a91`](https://github.com/oopnet/oopnet/commit/7370a91550cd8f472f9dac6aa9e08c773d84e8e9))

* Update python-app.yml ([`a24cd45`](https://github.com/oopnet/oopnet/commit/a24cd457185e22ca6690917995694dbf51f59220))

* refactor

- disabled some setup.py settings for now
- added seaborn to requirements again
- fixed some tests
- removed graph attribute from Network ([`6a1cffe`](https://github.com/oopnet/oopnet/commit/6a1cffeefb5b848fcb90ca2fdcf8228479a69179))

* Update python-app.yml ([`62d1a92`](https://github.com/oopnet/oopnet/commit/62d1a92439a59bfe002bd80c976991507eeb1f8b))

* Update python-app.yml ([`f5c5e74`](https://github.com/oopnet/oopnet/commit/f5c5e749fab831fb4f83cd4e35cb88405c507af8))

* Update python-app.yml ([`d70a457`](https://github.com/oopnet/oopnet/commit/d70a4575376fb0a4f1665643b46e1d4086e624b6))

* Update python-app.yml ([`87904cb`](https://github.com/oopnet/oopnet/commit/87904cb86342433af110c4217669ae35a5078376))

* Create python-app.yml ([`0d76bcb`](https://github.com/oopnet/oopnet/commit/0d76bcb4bf3e00f777dced16d0ee7286fb7d411e))

* Delete build_deploy.yml ([`5b4fe80`](https://github.com/oopnet/oopnet/commit/5b4fe80a02b6d4e90d49eeafea72fd119547b863))

* Create build_deploy.yml ([`4595a59`](https://github.com/oopnet/oopnet/commit/4595a595ae914eee8fe34b6d3f462f761791fb32))

* refactor

- refactored Pump attributes (dropped keyword value scheme)
- created plot() und bokehplot() instance methods for Network objects
- removed NetworkComponent hash method
- renamed Report to SimulationReport
- added some docs
- fixed helper functions in graph.py
- added get_inflow_nodes and get_inflow_node_ids functions
- refactored special_getters.py to topology_getters.py
- cleaned up utils.py
- some minor fixes
- removed traits and seaborn from requirements.txt ([`0643495`](https://github.com/oopnet/oopnet/commit/06434957f30b4bafd1323880b494ef686568bcbd))

* refactor

- added Vertices (reading, writing, plotting)
- added split function to Pipes
- added coordinates_2d property to Links
- fixed some imports
- finished Report class
- removed report_getter_functions.py with all functions
- added first (very basic) plotting test
- removed api.py
- removed pandasreport.py
- removed length function and adddummyjunction from utils.py ([`ac9dd23`](https://github.com/oopnet/oopnet/commit/ac9dd238f05b9c661d969c49fff1dee1e73279eb))

* refactoring

- implemented Report class with properties for flow, pressure, etc.
- adapted tests and examples accordingly ([`ab6daf5`](https://github.com/oopnet/oopnet/commit/ab6daf5e02528de2b758726909da8b81825ac5fc))

* refactor

- made `run`, `read` and `write` class/instance methods for `Network` class/objects and removed `Read`, `Write` and `Run` factories from `__init__.py` files
- refactored imports to prevent circular imports
- adapted examples and tests ([`7933aa1`](https://github.com/oopnet/oopnet/commit/7933aa19fd87f82da246ce003835995a5fd43337))

* refactor

- added setting description to Valve subclasses
- remove valve_type attribute (adjusted reader, writer and tests accordingly)
- enabled passing a string to read
- minor changes to benchmark stuff that we can also do in WNTR
- added a reset method to the benchmark ([`a4d7027`](https://github.com/oopnet/oopnet/commit/a4d7027e6232cc0df5c1c3694bab4e3256fc3715))

* Merge pull request #19 from oopnet/refactor

Refactor ([`26cd804`](https://github.com/oopnet/oopnet/commit/26cd80401e771486555508d5a89461997596bf8e))

* refactoring

- switched import statements in examples to `import oopnet as on` (issue #15) ([`1842bdc`](https://github.com/oopnet/oopnet/commit/1842bdcb86e77a5fbfa3acb92ac4ed49fee5f7bd))

* refactoring

- added MultiDiGraph test ([`1614c9e`](https://github.com/oopnet/oopnet/commit/1614c9e348bbff80a47d0b3bd1df8f3a3d4abb24))

* refactoring

- added MultiDiGraph to graph&#39;s module __init__.py ([`1f55824`](https://github.com/oopnet/oopnet/commit/1f558242fec37f42b3f58842bc2295404cd105ed))

* refactoring

- added ComponentRegistry and SuperComponentRegistry classes to handle NetworkComponent storage in Network objects
- moved check_id_exists functionality to ComponenRegistry
- adapted getters, adders, removers and tests
- removed check_exists argument from adders (everything will be checked
- added rename method to NetworkComponents
- ([`ccce9e5`](https://github.com/oopnet/oopnet/commit/ccce9e5e96d46dfbead9cb4144a9592b3c9cf2a2))

* refactoring

relates to issue #17
- added MultiDiGraph factory
- added warnings to Graph and DiGraph factories ([`9a56229`](https://github.com/oopnet/oopnet/commit/9a56229243983495f2212f61696b3a5e1c137066))

* refactoring

- added logging
- added timer decorator
- added tests for example scripts
- some docstring improvements
- added examples for error handling and logging
- removed inititialstatus attribute
- removed __deepcopy__ from network
- renamed network hashtables to make them private attributes
- improved EPANET error handling
- moved some reader stuff around
- added some missing default values for component attributes
- fixed Network class with fields as attributes
- fixed some tests
- fixed types of TestModel component attributes
- fixed examples ([`b90f5bc`](https://github.com/oopnet/oopnet/commit/b90f5bc912fb270fe2db97f73e4f315a073d18d4))

* refactoring

- removed enums and all traces of them
- switched _component_hash attr to not be included in equality checks
- bugfix for component IDs
- switched everything from `initialstatus` to `status`
- fixed status writing
- added very simple Writer test ([`f76b875`](https://github.com/oopnet/oopnet/commit/f76b8757879935be8133569464ffd86b72a1b54f))

* refactoring

- worked over utils.py ([`752c1e3`](https://github.com/oopnet/oopnet/commit/752c1e31b5c17f570065205912a00b3183ab6c8e))

* refactoring

- removed enums again
- redid some type hints (switched from e.g., Dict to dict)
- added some documentation
- updated some __init__.py
- worked over bokehplot.py
- fixed some testing bugs ([`2d0cbda`](https://github.com/oopnet/oopnet/commit/2d0cbdaa251a1389ad0bf01da50f1d42bd46d40d))

* refactoring

- refactored examples
- added placeholder for report settings example
- added test for examples ([`2b5eec1`](https://github.com/oopnet/oopnet/commit/2b5eec1d8a8f162870b578838f2c65c219ce9b59))

* refactoring

- removed redundant import in utils.__init__.py
- added pandas Series weights to Graphs
- added Graphs to API docs
- small changes to network_components.py
- added docs to ComponentReader factory classes
- corrected type hints for pandas getters in report_getter_functions.py
- added Graph tests ([`db21e40`](https://github.com/oopnet/oopnet/commit/db21e404f600866e2201a4616cf684bccf5d88c6))

* refactoring

- started refactoring input file reader ([`ad9e2ca`](https://github.com/oopnet/oopnet/commit/ad9e2ca378609ab34ac42c72f4e645a9374f9b6e))

* refactoring

- started implementing BinaryFileReader ([`bfc9983`](https://github.com/oopnet/oopnet/commit/bfc9983f829f4dfe13c22a1871e9984d64dbd4ee))

* refactoring

- removed NetworkComponent __str__ method
- writer and simulator bugfixes (due to enums)
- added CTown TestingModel ([`1354653`](https://github.com/oopnet/oopnet/commit/13546537ad909dceb9360b2d5e8bdc4d570014c4))

* refactoring

added plotting to benchmark ([`6bb4aea`](https://github.com/oopnet/oopnet/commit/6bb4aeaf38d2807e49a3f60169bb4b894423338b))

* refactoring

- flattened reader and writer directories
- redid all __init__.py files for proper structure + changed import statements accordingly
- used typing TYPE_CHECKING to circumvent circular imports due to type checking
- moved enums to enums.py (for now) ([`d96beda`](https://github.com/oopnet/oopnet/commit/d96beda3d427e0447315d9ac3af0db9ce8c97cca))

* refactoring

- fixed bug that converted 12 am to 12 pm in time settings
- replaced try/except clause in read_options
- refactored read_system_operation.py
- refactored write_options_and_reporting.py a little
- added and removed some todos
- added new TestModel for rule testing
- added tests for rules, curves, options, report, times and patterns ([`a5fb570`](https://github.com/oopnet/oopnet/commit/a5fb57041093cdec19704c1cf2a2220dd5096d41))

* refactoring

- implemented Enums for strings like &#39;CLOSED&#39;, &#39;OPEN&#39;, &#39;YES&#39;, ...
- adapted tests, reader and writer accordingly ([`dbef38b`](https://github.com/oopnet/oopnet/commit/dbef38b6fa20a3bb16f1361796e73a4041b94a55))

* refactoring

- made type hints for list getters for informative
- fixed simulation errors ([`71c3cec`](https://github.com/oopnet/oopnet/commit/71c3cec029d1071671fbb1d4e14ff40d23a6516f))

* refactoring

- renamed ComponentExistsException to ComponentExistsError ([`65d84b8`](https://github.com/oopnet/oopnet/commit/65d84b869ead6f1f306a668aa81a31ba62007e9a))

* refactoring

- added first enum for testing ([`f94e89c`](https://github.com/oopnet/oopnet/commit/f94e89ce12a85101946a03f69c453e7056919cc5))

* refactoring

- fixed EPANET simulation error catching ([`a37ae3e`](https://github.com/oopnet/oopnet/commit/a37ae3e37bf652d62e4de2d976c50811ac0a48a6))

* refactoring

- renamed ComponentExistsException to ComponentExistsError
- added Errors and ErrorManager for failed Simulations + tests ([`085af79`](https://github.com/oopnet/oopnet/commit/085af79c3af3d3438a49d15b1241d81070df7da1))

* refactoring

- removed dataclass slots decorators ([`7ac33ee`](https://github.com/oopnet/oopnet/commit/7ac33ee3dd1bf2396b994d79e313f5dda2bccace))

* refactoring

- added setting attribute to pumps (= pump speed)
- adapted get_initialstatus function
- adapted get_setting function
- adapted v_diameter function (+ some docstring corrections)
- adapted property_getter tests accordingly ([`605b078`](https://github.com/oopnet/oopnet/commit/605b078d486c78e3d4124692c752fdbda20d8d19))

* refactoring

- some more graph.py refactoring
- fixed ExistingModelTest unittests ([`2bc6db3`](https://github.com/oopnet/oopnet/commit/2bc6db31e30604c89b653c1127a32de92085b8e0))

* refactoring

- added adder function for rules
- removed keyword args for adders
- added getters for rule IDs, fixed get_rules
- switched to dictionaries for storing rules
- fixed converter
- added MicropolisModel for testing
- fixed type hints for Times
- fixed reader for patterns, rules
- added defaults for system operations class attributes
- some test refactoring ([`352cfbc`](https://github.com/oopnet/oopnet/commit/352cfbcc903ae9c1e53b55660b179334a0b1e871))

* refactoring

- fixed component ID setter
- disabled slots for OOPNET to work with python 3.9 again ([`70f62ce`](https://github.com/oopnet/oopnet/commit/70f62ce0ed41cdd59828e8d5e227ec5615917efe))

* refactoring

- added revert method to Links
- added Link test (reverting and renaming)
- fixed Graphs
- added Graph creation to benchmark.py ([`d032fa2`](https://github.com/oopnet/oopnet/commit/d032fa2a6026806c99833761a7432ee504b96b5f))

* refactoring

- fixed some bugs
- refactored graph.py
- created exceptions.py ([`af08d00`](https://github.com/oopnet/oopnet/commit/af08d0010cc4da41152cfba45f864be8da8ce655))

* refactoring

- made add_element.py more efficient and reduced boilerplate code
- switched (hopefully) all iterations in Read to element getter functions
- added slots=True to dataclasses (requires python 3.10)
- refactored NetworkComponents to simplify ID property setters
- added some element list getters
- minor refactoring of graph functions
- minor refactoring of pyplot.py
- minor fixes
- removed some checks like `if network.junctions` since junctions is always instantiated
- removed sortedcontainers from requirements.txt
- removed `is not None` where they don&#39;t make a difference
- disabled bulk, wall and tank writing for Reactions ([`d9dd48e`](https://github.com/oopnet/oopnet/commit/d9dd48e03b1ecbb3af0aaf80773fbd47c7ccbca8))

* update ([`a545441`](https://github.com/oopnet/oopnet/commit/a54544192d36c6992179148d9f61b07177d98cc5))

* worked over tests and added a benchmark ([`d39dbc7`](https://github.com/oopnet/oopnet/commit/d39dbc78f0caefa127d7874b3365808132ac1631))

* worked over examples ([`0c17cf3`](https://github.com/oopnet/oopnet/commit/0c17cf3801766d8418a910cff5a3dd29cfd974e4))

* refactoring

- switched to Google Docstrings
- redid adders and removers
- used adder functions in reader
- added some docs
- created ModelSimulator class
- added type hints
- removed `if network.junctions` and related checks
- added some todo comments
- worked over imports
- add sortedcontainers to requirements
- worked over setup.py (slightly) ([`aa2d292`](https://github.com/oopnet/oopnet/commit/aa2d292e4ac8c97ae72da4367e305d8a39e3b937))

* moved part of the function imports to dedicated __init__.py files ([`da94125`](https://github.com/oopnet/oopnet/commit/da94125501336012d1713b9020438b7dba30d5d9))

* replace epanet2d.exe (EPANET 2.0) with runepanet.exe (EPANET 2.2) ([`6baebdf`](https://github.com/oopnet/oopnet/commit/6baebdfb9ff752a83980d5699c06e14d49a46e62))

* remove traits, implement dataclasses and type hints instead, switched to Epanet 2.2, replace networkhash, add a few additional getters ([`feea28d`](https://github.com/oopnet/oopnet/commit/feea28d928f15aeebfcc23e8952616485f1e165f))

* move part of tests from GitLab branch epanet2_2 ([`6927d20`](https://github.com/oopnet/oopnet/commit/6927d20437d7d0604fc70886fed0659693a90631))

* initial commit of oopnet code of brachn python3 from gitlab.com ([`4d44a36`](https://github.com/oopnet/oopnet/commit/4d44a3669069137c6e1f1bdffd3f3a72f7996d43))

* added mac specific files to gitignore ([`e70ab2f`](https://github.com/oopnet/oopnet/commit/e70ab2f44bb6892b47ecdb71a54e25d347f5b388))

* Update README.md ([`bed7434`](https://github.com/oopnet/oopnet/commit/bed7434aabadd70d881bfe82782ed0dfb897ab12))

* Initial commit ([`923eb1d`](https://github.com/oopnet/oopnet/commit/923eb1d77063a6084a4a30fbb6e4885244e0080e))
