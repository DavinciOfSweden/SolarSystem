# SolarSystem
Scale* model of the solar system

*the distances are to scale, but the size of the planets are only scale relative to eachother. However, the code has been written such that everything is scale. 
A variable 'sizeGenerosity' has been added to increase the size of all planets, otherwise they would not be able to be seen.

Updates:

1) SolarSystemSave_18Nov2021.py
- added color to planets.
- added rings to saturn.
- added the asteroidBelt function and asteroid class, the asteroid belt can now be generated.

2) SolarSystemSave_22Nov2021.py
- added "units" to multiply with the relative scale so that "realism" of the proportions is true.
- sizeGenerosity and scale variables added to compensate for the, now very small planets.
- found out that it is standard practice to add, if "name" == __main__. So that was then added.

3) SolarSystemSave_14Dec2021.py
- camera movement was added by clicking on the screen, however it was very slow to render due to the large amounts of points making up the asteroid belts.

4) SolarSystemSave_20Jan2022.py
- Spacial partitioning was used as an attempt to reduce the render time; fairly succssesful, but improvement was not good enough.

5) SolarSystemSave_09Feb2022.py
- movement of planets were attempted, minor success, all speeds had the same angular displacement, which is not what was desired.


6) SolarSystem_Cleaned.py
- code was revamped due to several problems in the basis of the code (eg. earths moon wasn't pinned to earth, so position of moon wasn't able to be calculated relative to earths position.)
- movement of planets were successfully added, speed is to scale with real speeds.
