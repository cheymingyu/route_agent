from langchain_core.output_parsers import PydanticOutputParser
from .schemas import IntentSchema

parser = PydanticOutputParser(pydantic_object=IntentSchema)

format_instructions = parser.get_format_instructions()
