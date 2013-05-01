import java.io.*;
import java.util.*;


public class CPCClassify{
	static void rank(String line){
		StringTokenizer st = new StringTokenizer(line, ";");
		HashMap<String, Integer> cpcMap = new HashMap<String, Integer>();
		while(st.hasMoreTokens()){
			StringTokenizer st2 = new StringTokenizer(st.nextToken());	
			String cpc = st2.nextToken();
			Integer count = cpcMap.get(cpc);
			if(count==null){
				count = 1;				
			}else{
				count++;
			}
			cpcMap.put(cpc, count);
		}
		int[] counts = new int[cpcMap.keySet().size()];
		HashMap<Integer, LinkedList<String>> cpcRMap = new HashMap<Integer, LinkedList<String>>();
		int i = 0;
		for(String cpc:cpcMap.keySet()){
			int count = cpcMap.get(cpc);
			counts[i] = count;
			LinkedList<String> cpcs = cpcRMap.get(count);
			if(cpcs == null){
				cpcs = new LinkedList<String>();
			}
			cpcs.add(cpc);
			// System.out.printf("%s:%d ",cpc, cpcMap.get(cpc));
			cpcRMap.put(count, cpcs);
			i++;
		}
		Arrays.sort(counts);
		int n = 3;
		if(counts.length<3){
			n = counts.length;
		}
		i = counts.length-1;
		while(n>0){
			for(String cpc:cpcRMap.get(counts[i])){
				if(n>0){
					System.out.printf("%s,",cpc);
					n--;
				}else{
					break;
				}		
			}
			i--;
		}
		System.out.println("");
		// System.out.println("...");
	}
	public static void main(String[] args) throws IOException{
		try{
			BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
			String line = reader.readLine();
			while(line != null){
				if(line.length() > 0){
					rank(line);
				}else{
					System.out.println("");
				}	
				line = reader.readLine();
			}
		}catch(Exception e){
			System.err.println("error: "+e);
		}		
	}
}