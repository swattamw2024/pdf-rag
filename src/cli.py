import click

from src.rag_pipeline import RAGPipeline


@click.group()
@click.option("--collection", "-c", default="pdf_documents", help="ChromaDB collection name")
@click.pass_context
def cli(ctx, collection):
    """Offline PDF/DOCX RAG — ask questions about your local documents."""
    ctx.ensure_object(dict)
    ctx.obj["pipeline"] = RAGPipeline(collection_name=collection)


@cli.command()
@click.argument("path")
@click.pass_context
def ingest(ctx, path):
    """Ingest a PDF/DOCX file or a directory of documents."""
    pipeline = ctx.obj["pipeline"]
    click.echo(f"Ingesting: {path}")
    count = pipeline.ingest(path)
    click.echo(f"Done. {count} chunks indexed.")


@cli.command()
@click.argument("question")
@click.pass_context
def ask(ctx, question):
    """Ask a question about ingested documents."""
    pipeline = ctx.obj["pipeline"]
    result = pipeline.query(question)
    click.echo(f"\n{result['answer']}\n")
    if result["sources"]:
        click.echo("--- Sources ---")
        for s in result["sources"]:
            click.echo(f"  [{s['source']} p.{s['page']}] {s['text'][:100]}...")


@cli.command("list")
@click.pass_context
def list_collections(ctx):
    """List all document collections."""
    pipeline = ctx.obj["pipeline"]
    collections = pipeline.list_collections()
    if not collections:
        click.echo("No collections found.")
        return
    for name in collections:
        click.echo(f"  - {name}")


@cli.command()
@click.argument("name", required=False)
@click.pass_context
def clear(ctx, name):
    """Delete a collection (defaults to current)."""
    pipeline = ctx.obj["pipeline"]
    target = name or pipeline.collection_name
    if click.confirm(f"Delete collection '{target}'?"):
        pipeline.clear(target)
        click.echo(f"Deleted: {target}")


@cli.command()
@click.pass_context
def chat(ctx):
    """Interactive chat loop — ask questions until you type 'quit'."""
    pipeline = ctx.obj["pipeline"]
    doc_count = pipeline.doc_count()
    click.echo(f"Chat mode ({doc_count} chunks in store). Type 'quit' to exit.\n")

    while True:
        question = click.prompt("You", prompt_suffix="> ")
        if question.strip().lower() in ("quit", "exit", "q"):
            break
        result = pipeline.query(question)
        click.echo(f"\nAssistant: {result['answer']}\n")
        if result["sources"]:
            click.echo("  Sources:")
            for s in result["sources"]:
                click.echo(f"    [{s['source']} p.{s['page']}]")
            click.echo()


if __name__ == "__main__":
    cli()
