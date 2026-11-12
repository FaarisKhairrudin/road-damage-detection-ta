"""Lightweight completion/provenance gate; no model or projection imports."""
from pathlib import Path
import hashlib
import json

REQUIRED = ('inputs.json','manifest.csv','embeddings.npy','domains.npy','umap.npy','tsne.npy',
            'image_stats.csv','domain_medians.csv','samples_manifest.csv','umap.png','tsne.png','stats.png','samples.png')


def completed_bundle(directory):
    directory=Path(directory)
    status=directory/'run_status.json'
    if (directory/'INCOMPLETE.md').exists() or not status.is_file():
        return None
    if json.loads(status.read_text()).get('status')!='complete':
        return None
    provenance=directory/'provenance.json'
    if not provenance.is_file():
        raise ValueError('Completed domain run has no provenance.')
    record=json.loads(provenance.read_text())
    if record.get('embedding_shape',[None])[0]!=1302:
        raise ValueError('Completed domain run does not describe the frozen 1302-image split.')
    for name in REQUIRED:
        path=directory/name
        if not path.is_file() or record.get('outputs',{}).get(name)!=hashlib.sha256(path.read_bytes()).hexdigest():
            raise ValueError(f'Completed domain output is missing or changed: {name}')
    return record
