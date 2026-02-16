from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from ai.llm_client import LLMClient
from ai.rag.vector_store import VectorStore
from ai.tools.cost_calculator import CostCalculator
from bot.handlers.callbacks import on_callback
from bot.handlers.conversation import AIConversationHandler
from bot.handlers.start import help_command, start_command
from config import settings
from services.conversation_service import ConversationService
from services.lead_service import LeadService
from utils.logger import setup_logging


async def build_application() -> Application:
    """Собирает Telegram-приложение и регистрирует обработчики."""
    setup_logging(settings.log_level)

    llm = LLMClient(api_key=settings.openai_api_key, model=settings.openai_model)
    vector_store = VectorStore(
        persist_directory=settings.vector_db_path,
        embedding_model=settings.embedding_model,
    )
    calculator = CostCalculator(customs_data={}, shipping_data={})
    conversation_service = ConversationService()
    lead_service = LeadService()

    ai_handler = AIConversationHandler(
        llm_client=llm,
        vector_store=vector_store,
        calculator=calculator,
        conversation_service=conversation_service,
        lead_service=lead_service,
    )

    app = Application.builder().token(settings.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_handler.handle_message))
    return app


async def main() -> None:
    """Точка входа асинхронного приложения."""
    application = await build_application()
    await application.run_polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
