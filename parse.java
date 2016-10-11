import org.w3c.dom.*;
import javax.xml.parsers.*;
import java.io.*;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;

public class parse{

public static void main(String[] args){

try{
	DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
	DocumentBuilder builder = dbFactory.newDocumentBuilder();

	File inputFile = new File(args[0]);
	
	DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
	Document doc = dBuilder.parse(inputFile);
	
	NodeList nl =  doc.getElementsByTagName("name");

	for (int i=0; i < nl.getLength(); i++) {
		Node node = nl.item(i);
		if (node.getNodeType() == Node.ELEMENT_NODE) {
			System.out.println(node.getTextContent());
		}
	}

} catch (Exception e) {
  e.printStackTrace();
}

}
}
