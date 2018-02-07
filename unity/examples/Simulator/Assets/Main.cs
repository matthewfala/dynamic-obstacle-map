using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace AssemblyCSharp
{
	
public class Main : MonoBehaviour {
	private int maxItems;
		private int maxDir;
	Dictionary<int,GameObject> d;
	Random rnd = new Random();
	// Use this for initialization
	void Start () {
			d = new Dictionary<int,GameObject>();
			maxItems = 200;
			maxDir = 100;
	}
	
	// Update is called once per frame
	void Update () {
			print("update");
		Update up = getUpdate ();
			for (int i = 0; i < up.numItems; i++) 
			{
				GameObject v;
				if (!d.TryGetValue (up.getId(i), out v))
				{
					d[up.getId(i)]= ( GameObject.CreatePrimitive (PrimitiveType.Cube));
					d[up.getId(i)].AddComponent<Cubemind> ();
				}
				print("new");
				d[up.getId(i)].GetComponent<Cubemind>().newState(up.getState (i));


			}
	}
	Update getUpdate()
	{
		int n = (int) (Random.value * maxItems);
		State [] s = new State[n];
			int[] id = new int[n];
		for (int i = 0; i < n; i++) 
		{
			int idd =(int) (Random.value * maxItems); 
				id [i] = idd;
				GameObject v;
			if(d.TryGetValue(idd,out v ))
					s [i] = new State (d[idd].GetComponent<Cubemind>().state.x+(int)(Random.value * 3)-1,d[idd].GetComponent<Cubemind>().state.y+(int)(Random.value * 3)-1,d[idd].GetComponent<Cubemind>().state.z+(int)(Random.value * 3)-1);
			else
					s [i] = new State ((int)(Random.value * 2*maxDir-maxDir),(int)(Random.value * 2*maxDir-maxDir),(int)(Random.value * 2*maxDir-maxDir));
				if (s [i].x > maxDir)
					s [i].x = maxDir;
				if (s [i].y > maxDir)
					s [i].y = maxDir;
				if (s [i].z > maxDir)
					s [i].z = maxDir;
				if (s [i].x <-maxDir)
					s [i].x = -maxDir;
				if (s [i].y < -maxDir)
					s [i].y = -maxDir;
				if (s [i].z < -maxDir)
					s [i].z =- maxDir;
		}
		return new Update (n, s,id);
	}
}
}
