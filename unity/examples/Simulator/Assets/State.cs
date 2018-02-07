using System;

namespace AssemblyCSharp
{
	public class State
	{
		public int x,y,z;
		public State (int a, int b, int c)
		{
			x = a;
			y = b;
			z = c;
		}
		int [] getCoor()
		{
			return new int[] {x,y,z};
		}

	}
}

