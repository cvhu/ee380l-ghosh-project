import java.net.*;
import java.io.*;

public class WebCrawler{
	public static void main(String[] args) throws Exception{
		URL google = new URL("http://www.google.com");
		URLConnection gc = google.openConnection();
		BufferedReader reader = new BufferedReader(new InputStreamReader(gc.getInputStream()));
		String line;
		while((line=reader.readLine()) != null){
			System.out.println(line);
		}
		reader.close();
	}
}