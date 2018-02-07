using System;

namespace AssemblyCSharp
{
	public class Update
	{
		public int numItems;
		int [] id;
		State [] s;
		public Update (int n, State [] ss, int [] i)
		{
			id = i;
			s = ss;
			numItems = n;
		}
		public State getState(int n)
		{
			return s[n];
		}
		public int getId(int n)
		{
			return id[n];
		}
	}
}

