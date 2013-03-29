import java.io.*;
import java.util.*;

public class Synthesizer{
	static File csvFile;
	static File tmcFile;
	static HashMap<String, LinkedList<String>> tmcMap;
	static File cpctFile;
	static File taFile;
	static File summaryFile;
	public static void parseTMC(File file){
		BufferedReader reader = new BufferedReader(new FileReader(file));
		String line = reader.readLine();
		line = reader.readLine()
		while(line != null){
			StringTokenizer st = new StringTokenizer(line);
			st.nextToken();
			String path = st.nextToken();
			int patInd = path.indexOf("/pat");
			String 
		}
	}
	public static void main(String[] args) throws IOException{
		try{
			csvFile = new File(args[0]);
			tmcFile = new File(args[1]);
			parseTMC(tmcFile);
			cpctFile = new File(args[2]);
			taFile = new File(args[3]);
			summaryFile = new File(args[4]);
			
		}catch(Exception e){
			System.err.printf("Please use java Synthesizer *.csv *.tmc *.cpct *.ta *.summary")
		}
	}
}