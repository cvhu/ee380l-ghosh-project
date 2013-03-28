import org.jsoup.nodes.*;
import org.jsoup.select.*;
import org.jsoup.*;

import java.io.*;
import java.util.*;

class CPCCrawler{
	public static void main(String[] args) throws IOException{
		try{
			BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
			System.out.printf("Enter CPC Class Code>>");
			String line = stdin.readLine();
			String urlBase = "http://www.uspto.gov/web/patents/classification/cpc/html/cpc-";
			Connection connection;
			Document doc;
			String url;
			while(line!=null){
				url = urlBase+line+".html";
				try{
					connection  = Jsoup.connect(url);
					connection.timeout(20000);
					System.out.println("\n...url connected");
					doc = connection.get();					
					System.out.println(doc.select(".cpc-text").first().text());
				}catch(Exception e){
					System.err.printf("Error fetching url %s:%s\n",url,e);
				}
				System.out.printf("Enter CPC Class Code>>");
				line = stdin.readLine();
			}
		}catch(Exception e){
			System.err.println(e);
		}
	}
}