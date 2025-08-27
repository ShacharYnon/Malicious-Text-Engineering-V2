from kafka import KafkaConsumer
from pymongo import MongoClient, ASCENDING, errors
from datetime import datetime, timezone
from .. import config
import json
class InterestingConsumerService:
    def __init__(self) -> None:
        self._consumer = KafkaConsumer(
            config.KAFKA_TOPIC,
            bootstrap_servers=config.KAFKA_BOOTSTRAP,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            enable_auto_commit=False,
            auto_offset_reset=config.AUTO_OFFSET_RESET,
            group_id=config.GROUP_ID,
            max_poll_interval_ms=config.MAX_POLL_INTERVAL_MS,
            session_timeout_ms=config.SESSION_TIMEOUT_MS,
        )
        self._client = MongoClient(config.MONGO_URI, tz_aware=True, uuidRepresentation="standard")
        self._coll = self._client[config.MONGO_DB][config.COLLECTION_NAME]
        self._coll.create_index(
            [("topic", ASCENDING),("kafka_offset", ASCENDING)],
            unique=True
        )
        self._coll.create_index([("timestamp", ASCENDING)])

    @property
    def consumer(self) -> KafkaConsumer:
        return self._consumer

    @property
    def collection(self):
        return self._coll

    def consume_once(self, max_records: int = 10, poll_timeout_ms: int = 200) -> int:
        """
        Consume up to `max_records` and return how many were stored.
        Designed to be called from an HTTP endpoint without blocking.
        """
        consumed = 0
        records = self._consumer.poll(timeout_ms=poll_timeout_ms, max_records=max_records)

        for tp, msgs in records.items():
            for msg in msgs:
                try:
                    doc = {
                        "topic": msg.topic,
                        "offset": msg.offset,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "value": msg.value,
                    }
                    self._coll.insert_one(doc)
                    consumed += 1
                except errors.DuplicateKeyError:
                    pass
                except Exception as e:
                    continue

        if consumed:
            self._consumer.commit()

        return consumed