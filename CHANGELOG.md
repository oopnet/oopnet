# Changelog

<!--next-version-placeholder-->

## v0.5.3 (2022-10-05)
### Fix
* Bugfix in ReportFileReader ([`2dad842`](https://github.com/oopnet/oopnet/commit/2dad8422c260974d81b9da04a60e21475ae3c6fd))

## v0.5.2 (2022-09-26)
### Fix
* ReportFileReader bugfix ([`127f1ce`](https://github.com/oopnet/oopnet/commit/127f1cec0a47a7ab1b6932a5701085be961f0a86))

## v0.5.1 (2022-09-22)
### Fix
* Fixed demand category bug ([`e150b00`](https://github.com/oopnet/oopnet/commit/e150b00c63e3c1e159a089731a2b77566befa380))

## v0.5.0 (2022-09-18)
### Feature
* Added a new NetworkPlotter class that enables static plots and animations ([`3a3a028`](https://github.com/oopnet/oopnet/commit/3a3a02840443009cffb2d9d271402bb4c7123855))
* Added `center` method to Link components to calculate a Link's geometric center in 2D ([`d3f5dbf`](https://github.com/oopnet/oopnet/commit/d3f5dbff5f5e7f2e175206fa7a6b2d7fb020711f))

### Fix
* Switched SimulationReport property type hints to Union[pd.Series, pd.DataFrame] to take extended period simulations into account ([`2ffcccc`](https://github.com/oopnet/oopnet/commit/2ffcccc635849a9528fb76e46f7a64dacef4e99f))

### Documentation
* Renamed LICENSE to LICENSE.md to use markdown ([`08a1e69`](https://github.com/oopnet/oopnet/commit/08a1e6958e4ff9444ba9d9f209893cd6630bc932))

## v0.4.1 (2022-09-02)
### Fix
* Added sort_index() call to pandas results ([`53545ca`](https://github.com/oopnet/oopnet/commit/53545ca621afce3b6f36663100e9228e306c788f))

## v0.4.0 (2022-09-01)
### Feature
* Added vertex plotting to Bokeh plot ([`4ebe022`](https://github.com/oopnet/oopnet/commit/4ebe02261672f06268f9d666f869e62ffcb5b73c))

### Fix
* Switched condition attribute default of Rules from None to an empty list ([`aad8f00`](https://github.com/oopnet/oopnet/commit/aad8f00bb9095cee65967e5f6ba52a03c0e15273))
* Fixed reading time options in hh:mm:ss format ([`fa2abef`](https://github.com/oopnet/oopnet/commit/fa2abef883af201a91924b4396a7221ca2389caa))

### Documentation
* Updated information in setup.cfg for PyPI ([`e6f23b5`](https://github.com/oopnet/oopnet/commit/e6f23b52a28b0b10475179221a91c550d6e9064b))
* Added badges to README.md ([`d131b8a`](https://github.com/oopnet/oopnet/commit/d131b8adbac0e361ca12809c2ee856cf7b834bee))

## v0.3.2 (2022-08-26)
### Fix
* Fixed concatenated large number parsing error in report file reader ([`1685835`](https://github.com/oopnet/oopnet/commit/1685835e1d16bf7eaa605e829486ddde07e4d5de))
* Moved parts of report module to simulator module for better consistency ([`41ca790`](https://github.com/oopnet/oopnet/commit/41ca7907043fd718c40fc0c5bf060bdba37be7e9))

### Documentation
* Corrected Network attribute documentation ([`3a71dd9`](https://github.com/oopnet/oopnet/commit/3a71dd9c26ee3aae277b80cc524dc313d662dd8c))

## v0.3.1 (2022-04-14)
### Fix
* Fixed a bug where networkx get_edge_data returning a dict instead of a list breaks nxedge2onlink_id ([`8377d16`](https://github.com/oopnet/oopnet/commit/8377d16a09b0e9a23820db2af7820fa627242a1f))

## v0.3.0 (2022-02-28)
### Feature
* Added get_by_id method to SuperComponentRegistry for NetworkComponent lookup ([`d89c8cc`](https://github.com/oopnet/oopnet/commit/d89c8cc88bb7ab979ec73a0a7b8e3d18c1c40d49))

### Fix
* Renamed Tank attribute diam to diameter ([`0f6801d`](https://github.com/oopnet/oopnet/commit/0f6801d03d755ba2e5ef85773309a2e0af5fed03))
* Fixed some type hints ([`91b3a6e`](https://github.com/oopnet/oopnet/commit/91b3a6eda9fae12a07e36adcbb91b527cab3c9ed))

## v0.2.3 (2022-02-22)
### Fix
* Fixed ComponentRegistry pickling ([`fbe2900`](https://github.com/oopnet/oopnet/commit/fbe290064dd353fdca969630cbfa6acac525c106))

## v0.2.2 (2022-02-22)
### Fix
* Disabled testing the mc stereo scoop example ([`003f249`](https://github.com/oopnet/oopnet/commit/003f249099a40d6b5c647571c0b8ef48f3be8fca))
* Fixed CI pipeline ([`50f2650`](https://github.com/oopnet/oopnet/commit/50f2650ea56249cb58d247210d41443c2d194283))
* Fixed CI pipeline ([`b79726c`](https://github.com/oopnet/oopnet/commit/b79726cbda8e37cd1cd9c675146f3b43cf67b15a))
* Fixed ComponentRegistry initialization ([`1cd7d64`](https://github.com/oopnet/oopnet/commit/1cd7d64184856de6b2633a1ceda4dbc2038e3ebe))

## v0.2.1 (2022-02-17)
### Fix
* Fixed writing Tank volumecurves ([`960a232`](https://github.com/oopnet/oopnet/commit/960a23287042eb8f20012748c4fbbca38f959a7e))

## v0.2.0 (2022-02-14)
### Feature
* Added linkwidth argument to Network.plot ([`f749a48`](https://github.com/oopnet/oopnet/commit/f749a4803e5583bea126791ed2c54e28a1059b6f))

## v0.1.6 (2022-02-07)
### Fix
* Minor changes to setup.cfg to trigger release ([`18b3df2`](https://github.com/oopnet/oopnet/commit/18b3df2a166bd0ae575b128d0f5753755428acc1))

## v0.1.5 (2022-02-07)
### Fix
* Fix CI ([`98053e7`](https://github.com/oopnet/oopnet/commit/98053e7775ce0d87a239ea991e4905070f8a463f))

## v0.1.4 (2022-02-06)
### Fix
* Another setup.cfg fix ([`40e8eb8`](https://github.com/oopnet/oopnet/commit/40e8eb81d6a87839029de4566861539cd6d067c6))

## v0.1.3 (2022-02-06)
### Fix
* Moved requirements from requirements.txt to setup.cfg to enable autoinstall of missing packages ([`eb119cd`](https://github.com/oopnet/oopnet/commit/eb119cd954d35f4ad49b1625651d3a2167e5c7a7))

## v0.1.2 (2022-02-06)
### Fix
* Fixed setup.cfg package_data ([`c3f7122`](https://github.com/oopnet/oopnet/commit/c3f71223641b51a31b4e6e9282436480190a598b))

## v0.1.1 (2022-02-06)
### Fix
* Fixed setup.cfg license ([`4accf2d`](https://github.com/oopnet/oopnet/commit/4accf2d1038e4755bb5ec64b97c082f23376f2eb))

## v0.1.0 (2022-02-06)
### Feature
* Nonsense to create new release ([`617dee9`](https://github.com/oopnet/oopnet/commit/617dee993de458a42b374bc61a3eee834f699beb))
