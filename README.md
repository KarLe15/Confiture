<p>this is a project for university</p>
<p>This project by UPMC (Univeersité Pierre et Marie Curie).</p>
<h2>Confiture</h2>
<p>
This project answers the following problematic:
We have a quantity N decaliter of jam and pots of 'k' different volume (we suppose that we have an infinity of each volume and that we always have 1 decaliter jars).
and we want to keep the jam in jars knowing that a jar must be filled to the maximum to avoid fermentation.
</p>
for exemple :
<p>We have 10 decaliter of jam and we have 3 kind of jars [1, 5, 8] decaliter.</p>
<p>To solve this problem, I used 3 different approaches:</p>
<ul>
<li>The exhaustive research.</li>
<li>Dynamic programming.</li>
<li>A Glutton algorithm.</li>
</ul>
<p>The exhaustive search is too time and space consuming in the execution stack. It is therefore not a viable solution.</p>
<p>Dynamic prorammation, on the other hand, has a very fast execution but consumes a lot of memory quite quickly.</p>
<p>The Glutton algorithm is very fast and consumes very little memory but unfortunately does not give the optimal solution for all jam jar configurations.</p>
<p>Indeed, in the previous example the optimal solution is 2 ([5,5]);but the solution returned by the glutton algorithm is 3 ([ 8, 1, 1])</p>
