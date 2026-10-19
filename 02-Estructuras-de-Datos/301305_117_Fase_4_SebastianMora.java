def ejecutar_fase4(self):
    try:
        # Verificar si el archivo Java existe
        archivo_java = "301305_117_Fase_4_SebastianMora.java"
        
        if not os.path.exists(archivo_java):
            # Si no existe, crear el archivo Java automáticamente
            self.crear_archivo_java()
            messagebox.showinfo("Éxito", f"Archivo Java creado: {archivo_java}\n\nAhora puede ejecutar la Fase 4")
            return
        
        # Crear archivo batch para ejecución automática
        batch_content = '''@echo off
echo ============================================
echo    FASE 4 - ARBOL BINARIO JAVA
echo    Curso: Estructura de Datos - 301305
echo ============================================
echo.
echo Compilando aplicacion Java...
javac 301305_117_Fase_4_SebastianMora.java

if %errorlevel% == 0 (
    echo.
    echo ¡Compilacion exitosa!
    echo Ejecutando aplicacion...
    echo.
    java BinaryTreeApp
) else (
    echo.
    echo ERROR: No se pudo compilar el archivo Java
    echo.
    echo Verifique que:
    echo 1. Tiene Java JDK instalado
    echo 2. La variable de entorno JAVA_HOME esta configurada
    echo 3. El archivo Java esta en la misma carpeta
    echo.
    pause
)
'''
        
        with open('ejecutar_fase4.bat', 'w') as f:
            f.write(batch_content)
        
        # Ejecutar el batch
        subprocess.Popen(['ejecutar_fase4.bat'], shell=True)
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ejecutar la Fase 4: {str(e)}")

def crear_archivo_java(self):
    """Crea automáticamente el archivo Java si no existe"""
    java_code = '''import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;

// Binary Tree Application - UNAD Fase 4
// Estructura de Datos - 301305
// Estudiante: Sebastián Daniel Mora Insuasti

class TreeNode {
    int data;
    TreeNode left;
    TreeNode right;
    
    public TreeNode(int data) {
        this.data = data;
        this.left = null;
        this.right = null;
    }
}

class BinaryTree {
    private TreeNode root;
    
    public BinaryTree() {
        root = null;
    }
    
    // Insertar nodo
    public void insert(int data) {
        root = insertRec(root, data);
    }
    
    private TreeNode insertRec(TreeNode root, int data) {
        if (root == null) {
            root = new TreeNode(data);
            return root;
        }
        
        if (data < root.data) {
            root.left = insertRec(root.left, data);
        } else if (data > root.data) {
            root.right = insertRec(root.right, data);
        }
        
        return root;
    }
    
    // Eliminar nodo
    public void delete(int data) {
        root = deleteRec(root, data);
    }
    
    private TreeNode deleteRec(TreeNode root, int data) {
        if (root == null) return root;
        
        if (data < root.data) {
            root.left = deleteRec(root.left, data);
        } else if (data > root.data) {
            root.right = deleteRec(root.right, data);
        } else {
            if (root.left == null) {
                return root.right;
            } else if (root.right == null) {
                return root.left;
            }
            
            root.data = minValue(root.right);
            root.right = deleteRec(root.right, root.data);
        }
        
        return root;
    }
    
    private int minValue(TreeNode root) {
        int minValue = root.data;
        while (root.left != null) {
            minValue = root.left.data;
            root = root.left;
        }
        return minValue;
    }
    
    // Buscar nodo
    public boolean search(int data) {
        return searchRec(root, data);
    }
    
    private boolean searchRec(TreeNode root, int data) {
        if (root == null) return false;
        if (root.data == data) return true;
        
        if (data < root.data) {
            return searchRec(root.left, data);
        } else {
            return searchRec(root.right, data);
        }
    }
    
    // Recorridos
    public List<Integer> inOrder() {
        List<Integer> result = new ArrayList<>();
        inOrderRec(root, result);
        return result;
    }
    
    private void inOrderRec(TreeNode root, List<Integer> result) {
        if (root != null) {
            inOrderRec(root.left, result);
            result.add(root.data);
            inOrderRec(root.right, result);
        }
    }
    
    public List<Integer> preOrder() {
        List<Integer> result = new ArrayList<>();
        preOrderRec(root, result);
        return result;
    }
    
    private void preOrderRec(TreeNode root, List<Integer> result) {
        if (root != null) {
            result.add(root.data);
            preOrderRec(root.left, result);
            preOrderRec(root.right, result);
        }
    }
    
    public List<Integer> postOrder() {
        List<Integer> result = new ArrayList<>();
        postOrderRec(root, result);
        return result;
    }
    
    private void postOrderRec(TreeNode root, List<Integer> result) {
        if (root != null) {
            postOrderRec(root.left, result);
            postOrderRec(root.right, result);
            result.add(root.data);
        }
    }
    
    public TreeNode getRoot() {
        return root;
    }
}

class TreePanel extends JPanel {
    private BinaryTree tree;
    private final Map<TreeNode, Point> nodePositions;
    private static final int NODE_RADIUS = 20;
    private static final int VERTICAL_GAP = 60;
    
    public TreePanel(BinaryTree tree) {
        this.tree = tree;
        this.nodePositions = new HashMap<>();
        setPreferredSize(new Dimension(800, 600));
        setBackground(Color.WHITE);
    }
    
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        nodePositions.clear();
        TreeNode root = tree.getRoot();
        if (root != null) {
            calculateNodePositions(root, getWidth() / 2, 50, getWidth() / 4);
            drawTree(g2d, root);
        }
    }
    
    private void calculateNodePositions(TreeNode node, int x, int y, int offset) {
        if (node == null) return;
        
        nodePositions.put(node, new Point(x, y));
        
        if (node.left != null) {
            calculateNodePositions(node.left, x - offset, y + VERTICAL_GAP, offset / 2);
        }
        if (node.right != null) {
            calculateNodePositions(node.right, x + offset, y + VERTICAL_GAP, offset / 2);
        }
    }
    
    private void drawTree(Graphics2D g2d, TreeNode node) {
        if (node == null) return;
        
        Point currentPos = nodePositions.get(node);
        
        // Dibujar líneas a los hijos
        if (node.left != null) {
            Point leftPos = nodePositions.get(node.left);
            g2d.setColor(Color.BLACK);
            g2d.drawLine(currentPos.x, currentPos.y, leftPos.x, leftPos.y);
        }
        if (node.right != null) {
            Point rightPos = nodePositions.get(node.right);
            g2d.setColor(Color.BLACK);
            g2d.drawLine(currentPos.x, currentPos.y, rightPos.x, rightPos.y);
        }
        
        // Dibujar nodo
        g2d.setColor(Color.CYAN);
        g2d.fillOval(currentPos.x - NODE_RADIUS, currentPos.y - NODE_RADIUS, 
                     NODE_RADIUS * 2, NODE_RADIUS * 2);
        g2d.setColor(Color.BLACK);
        g2d.drawOval(currentPos.x - NODE_RADIUS, currentPos.y - NODE_RADIUS, 
                     NODE_RADIUS * 2, NODE_RADIUS * 2);
        
        // Dibujar valor del nodo
        g2d.setColor(Color.BLACK);
        g2d.setFont(new Font("Arial", Font.BOLD, 12));
        String text = String.valueOf(node.data);
        FontMetrics fm = g2d.getFontMetrics();
        int textWidth = fm.stringWidth(text);
        g2d.drawString(text, currentPos.x - textWidth / 2, currentPos.y + 5);
        
        // Dibujar hijos recursivamente
        drawTree(g2d, node.left);
        drawTree(g2d, node.right);
    }
    
    public void updateTree(BinaryTree newTree) {
        this.tree = newTree;
        repaint();
    }
}

public class BinaryTreeApp extends JFrame {
    private final BinaryTree tree;
    private TreePanel treePanel;
    private JTextField inputField;
    private JTextArea outputArea;
    
    public BinaryTreeApp() {
        tree = new BinaryTree();
        initializeGUI();
    }
    
    private void initializeGUI() {
        setTitle("Binary Tree Visualizer - UNAD Fase 4 - Integrado");
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLayout(new BorderLayout());
        
        // Panel principal
        JPanel mainPanel = new JPanel(new BorderLayout());
        
        // Panel de visualización del árbol
        treePanel = new TreePanel(tree);
        JScrollPane scrollPane = new JScrollPane(treePanel);
        mainPanel.add(scrollPane, BorderLayout.CENTER);
        
        // Panel de control
        JPanel controlPanel = createControlPanel();
        mainPanel.add(controlPanel, BorderLayout.SOUTH);
        
        // Panel de salida
        JPanel outputPanel = createOutputPanel();
        mainPanel.add(outputPanel, BorderLayout.EAST);
        
        add(mainPanel);
        pack();
        setLocationRelativeTo(null);
        setVisible(true);
    }
    
    private JPanel createControlPanel() {
        JPanel panel = new JPanel(new FlowLayout());
        panel.setBorder(BorderFactory.createTitledBorder("Operaciones del Arbol - Fase 4"));
        
        inputField = new JTextField(10);
        panel.add(new JLabel("Valor:"));
        panel.add(inputField);
        
        JButton insertButton = new JButton("Insertar");
        JButton deleteButton = new JButton("Eliminar");
        JButton searchButton = new JButton("Buscar");
        JButton inOrderButton = new JButton("In-Order");
        JButton preOrderButton = new JButton("Pre-Order");
        JButton postOrderButton = new JButton("Post-Order");
        JButton clearButton = new JButton("Limpiar");
        JButton volverButton = new JButton("Volver al Menu");
        
        panel.add(insertButton);
        panel.add(deleteButton);
        panel.add(searchButton);
        panel.add(inOrderButton);
        panel.add(preOrderButton);
        panel.add(postOrderButton);
        panel.add(clearButton);
        panel.add(volverButton);
        
        // Action listeners
        insertButton.addActionListener(e -> insertNode());
        deleteButton.addActionListener(e -> deleteNode());
        searchButton.addActionListener(e -> searchNode());
        inOrderButton.addActionListener(e -> showTraversal("In-Order", tree.inOrder()));
        preOrderButton.addActionListener(e -> showTraversal("Pre-Order", tree.preOrder()));
        postOrderButton.addActionListener(e -> showTraversal("Post-Order", tree.postOrder()));
        clearButton.addActionListener(e -> clearOutput());
        volverButton.addActionListener(e -> dispose());
        
        return panel;
    }
    
    private JPanel createOutputPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setPreferredSize(new Dimension(250, 400));
        panel.setBorder(BorderFactory.createTitledBorder("Salida - Fase 4"));
        
        outputArea = new JTextArea(20, 20);
        outputArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(outputArea);
        panel.add(scrollPane, BorderLayout.CENTER);
        
        return panel;
    }
    
    private void insertNode() {
        try {
            int value = Integer.parseInt(inputField.getText());
            tree.insert(value);
            treePanel.updateTree(tree);
            outputArea.append("Insertado: " + value + "\\n");
            inputField.setText("");
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Por favor ingrese un numero entero valido");
        }
    }
    
    private void deleteNode() {
        try {
            int value = Integer.parseInt(inputField.getText());
            tree.delete(value);
            treePanel.updateTree(tree);
            outputArea.append("Eliminado: " + value + "\\n");
            inputField.setText("");
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Por favor ingrese un numero entero valido");
        }
    }
    
    private void searchNode() {
        try {
            int value = Integer.parseInt(inputField.getText());
            boolean found = tree.search(value);
            String message = found ? "Valor " + value + " ENCONTRADO en el arbol" 
                                 : "Valor " + value + " NO encontrado en el arbol";
            outputArea.append(message + "\\n");
            inputField.setText("");
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Por favor ingrese un numero entero valido");
        }
    }
    
    private void showTraversal(String type, List<Integer> traversal) {
        outputArea.append(type + ": " + traversal.toString() + "\\n");
    }
    
    private void clearOutput() {
        outputArea.setText("");
    }
    
    public static void main(String[] args) {
        // Mensaje en consola
        System.out.println("=== Arbol Binario UNAD Fase 4 ===");
        System.out.println("Curso: Estructura de Datos - 301305");
        System.out.println("Aplicacion iniciada...");
        
        // Ejecutar interfaz grafica
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                new BinaryTreeApp();
            }
        });
    }
}
'''
        
        with open("301305_117_Fase_4_SebastianMora.java", "w", encoding="utf-8") as f:
            f.write(java_code)