
from scipy import weave

class ScipyExample:
    """Example on how to use scipy.weave inside filters.
        The code loop inside the entire image 
        and reduce the value of each pixels by half"""
    
    def __init__(self):
        pass

    def execute(self, image):
        code = """
            int rows = Nimage[0];
            int cols = Nimage[1];
            int depth = Nimage[2];   
            for (int i=0; i < rows; i++)
            {
                for (int j=0; j < cols; j++)
                {
                    for (int k=0; k< depth; ++k)
                    {
                        image[(i*cols + j)*depth + k] /= 5;
                    }
                }
            }
            """
        
        weave.inline(code, ['image'])
        return image

