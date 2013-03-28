import org.jsoup.nodes.*;
import org.jsoup.select.*;
import org.jsoup.*;

import java.io.*;
import java.util.*;

//java Crawler input.csv output.csv dir

public class MCrawler{
	static int count = 0;
	static OutputStream outst;
	static String dir;
	
	public static void tokenize(String line, LinkedList<String> ll){
		int i = line.indexOf(',');		
		while(i >= 0){
			// System.out.println(i);
			if(i==0){
				ll.add("");
				line = line.substring(i+1);
			}else{
				ll.add(line.substring(0, i));
				line = line.substring(i+1);
			}			
			i = line.indexOf(",");
		}
		ll.add(line);
		System.out.println(ll.size());
	}
	public static void crawl(String line, OutputStream o){
		// StringTokenizer st = new StringTokenizer(line, ",");		
		// System.out.println("tokenized "+st.countTokens());
		String pid = "pat"+count;
		count++;
		LinkedList<String> ll = new LinkedList<String>();
		tokenize(line.replace("\"","").replace("(","").replace(")",""), ll);		
		String pn = ll.get(0);
		String ta = ll.get(1);
		String city = ll.get(2);
		String state = ll.get(3);
		String country = ll.get(4);
		String url = ll.get(5);
		if(ll.size()>6){
			state = ll.get(4);
			country = ll.get(5);
			url = ll.get(6);
		}
		String status = "";
		String cpc_class = "";	
		System.out.println("tokenization finished");	
		try{
			Connection connection = Jsoup.connect(url);
			connection.timeout(20000);
			System.out.println("connected");
			Document doc = connection.get();
			status = "valid";
			try{
				cpc_class = doc.getElementsContainingOwnText("CPC Class:").get(0).parent().nextElementSibling().text().replace(",", " ");			
				System.out.println("crawled cpc");
			}catch(Exception e){
				status = "no CPC";
				System.err.println("CPC doesn't exist");
			}
			
			File file;
			FileOutputStream fo;
			System.out.printf("writing %s ...\n", pid);
			try{
				file = new File(dir+"/"+pid+".txt");
				fo = new FileOutputStream(file);
				String t = doc.select("center>b").get(0).parent().nextElementSibling().text();
				String text = doc.text();
				int ci = text.indexOf("Claims");
				int di = text.indexOf("Description");
			 	t = t+"\n"+text.substring(ci, di);
				fo.write(t.getBytes());
				fo.close();				
			}catch(Exception e){
				status = "no abstract or claims";
				System.err.println("Cannot find abstract or claims: "+e);
			}		
		}catch(Exception e){
			status = "invalid url";
			System.err.println("invalid url "+e);
		}
				
		try{
			String outLine = pid+","+pn+","+ta+","+city+","+state+","+country+","+url+","+status+","+cpc_class+"\n";
			// System.out.println(outLine.getBytes());
			o.write(outLine.getBytes());
		}catch(Exception e){
			System.err.println("cannot write output"+e);
		}
	}
	
	
	public static void main(String[] args) throws IOException{
		try{			
			File input = new File(args[0]);
			System.out.println("read input");
			File output = new File(args[1]);
			System.out.println("read output");
			dir = args[2];
			System.out.println("read dir");
			OutputStream outst = new FileOutputStream(output);
			System.out.println("create out stream");
			String header = "pid, patent #, tech area, city, state, country, url, status, cpc_class\n";
			outst.write(header.getBytes());
			System.out.println("read header");
			BufferedReader reader = new BufferedReader(new FileReader(input));
			System.out.println("read input line");
			String line = reader.readLine();
			while(line != null){
				// System.out.println("crawl "+line);
				crawl(line, outst);
				line = reader.readLine();
			}
		}catch(Exception e){
			System.err.println("invalid input command "+e);
		}
	}
}